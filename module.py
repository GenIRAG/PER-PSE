import re
import json
import itertools
from datetime import datetime
import networkx as nx
from networkx.algorithms.isomorphism import DiGraphMatcher

from flashrag.config.config import Config
from flashrag.utils.utils import get_generator
from prompt import *
from flashrag.prompt import PromptTemplate
from flashrag.utils import str2json


openai_config_dict = {
    "framework": "openai",
    "generator_model": "gpt-4o-mini-2024-07-18",
    "generator_max_input_len": 5000,
    "generator_batch_size": 4,
    "generation_params": {
        "do_sample": False,
        "temperature": 0.0,
        "max_tokens": 1024
    },

    "openai_setting": {
        "base_url": "YOUR_URL",
        "api_key": "YOUR_KEY"
    }
}


def have_not_support_word(answer):
    not_support_words = ["support", "describe", "unclear", "insufficient", "unspecified", "mention", "evidence", "undefined", "none"]
    if any(ns_word in answer.lower() for ns_word in ["[]", "[ ]", "not "]):
        return True
    
    answer_words = re.split(r'[\s,.?!]+', answer)
    if any(ans_word.lower() in not_support_words for ans_word in answer_words):
        return True
    
    return False


class PERDPPlanner:
    def __init__(self, config, generator):
        self.config = config
        self.generator = generator
        self.dataset_name = self.config["dataset_name"]
        self.split = self.config["split"]

    def complete(self, item):
        def tag_map(value, tags):
            for s_tag, t_tag in tags.items():
                value = [v.replace(s_tag, t_tag) for v in value]
            return value

        def judge_type(graph, plan):
            graph_ = nx.DiGraph()
            for mid, meta in plan.items():
                graph_.add_node(mid)
                template, tag = meta[0], meta[1]
                pattern = r"<A(\d+)>"
                placeholders = re.findall(pattern, template)

                for placeholder in placeholders:
                    graph_.add_edge(f"Q{placeholder}", f"Q{re.findall(pattern, tag)[0]}")

            is_type = nx.is_isomorphic(graph_, graph)
            return is_type
        
        question = item.question
        graph = nx.DiGraph()

        if self.config["dataset_name"] in ["2wikimultihopqa", "musique"]:
            tips = json.dumps(item.metadata["question_decomposition"])

        elif self.config["dataset_name"] == "hotpotqa":
            supports = item.metadata["supporting_facts"]
            supports2str = [f"{support[0]}: {' '.join(support[1])}" for support in supports]
            tips = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(supports2str)])

        # Prompt Initialize
        if self.config["split"][0].split("_")[0] == "t1":
            if self.dataset_name == "hotpotqa":
                template = PromptTemplate(
                    config=self.config,
                    system_prompt=TYPE1_2HOP_BRIDGE_FOR_HOTPOTQA_SYSTEM_PROMPT,
                    user_prompt="Question: {question}\nTips: {tips}\nOutput: ",
                )
            else:
                template = PromptTemplate(
                    config=self.config,
                    system_prompt=TYPE1_2HOP_BRIDGE_SYSTEM_PROMPT,
                    user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
                )
            graph.add_edges_from([("Q1", "Q2")])

        elif self.config["split"][0].split("_")[0] == "t2":
            if self.dataset_name == "hotpotqa":
                template = PromptTemplate(
                    config=self.config,
                    system_prompt=TYPE2_2HOP_COMPARISON_FOR_HOTPOTQA_SYSTEM_PROMPT,
                    user_prompt="Question: {question}\nTips: {tips}\nOutput: ",
                )
            else:
                template = PromptTemplate(
                    config=self.config,
                    system_prompt=TYPE2_2HOP_COMPARISON_SYSTEM_PROMPT,
                    user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
                )
            graph.add_nodes_from(["Q1", "Q2"])

        elif self.config["split"][0].split("_")[0] == "t3":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE3_2HOP_INFERENCE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q2")])
            
        elif self.config["split"][0].split("_")[0] == "t4":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE4_3HOP_BRIDGE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q2"), ("Q2", "Q3")])

        elif self.config["split"][0].split("_")[0] == "t5":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE5_3HOP_BRIDGE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q3"), ("Q2", "Q3")])

        elif self.config["split"][0].split("_")[0] == "t6":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE6_4HOP_BRIDGE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q2"), ("Q2", "Q3"), ("Q3", "Q4")])

        elif self.config["split"][0].split("_")[0] == "t7":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE7_4HOP_BRIDGE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q3"), ("Q2", "Q3"), ("Q3", "Q4")])

        elif self.config["split"][0].split("_")[0] == "t8":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE8_4HOP_BRIDGE_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q2"), ("Q2", "Q4"), ("Q3", "Q4")])

        elif self.config["split"][0].split("_")[0] == "t9":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE9_4HOP_COMPARISON_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_nodes_from(["Q1", "Q2", "Q3", "Q4"])

        elif self.config["split"][0].split("_")[0] == "t10":
            template = PromptTemplate(
                config=self.config,
                system_prompt=TYPE10_4HOP_BRIDGE_COMPARISON_SYSTEM_PROMPT,
                user_prompt="Question: {question}\nTips: ```json{tips}```\nOutput: ",
            )
            graph.add_edges_from([("Q1", "Q3"), ("Q2", "Q4")])

        prompt = [template.get_string(question=question, tips=tips)]
        result = str2json(self.generator.generate(prompt)[0])

        # Tag Formatting
        tags = {f"#{i+1}": f"<A{i+1}>" for i in range(len(result))}
        plan = {k: tag_map(v, tags) for k, v in result.items()}

        is_type = judge_type(graph, plan)
        item.update_output("is_type", is_type)
        if is_type:
            item.metadata["plan"] = plan
        else:
            item.metadata["plan"] = {}


class PERDPExecutor:
    def __init__(self, config, generator):
        self.config = config
        self.generator = generator
        self.dataset_name = self.config["dataset_name"]
        self.split = self.config["split"]

        self.relevant_template = PromptTemplate(
            config=config,
            system_prompt=GOLDEN_RELEVANT_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nRetrievals:\n{paragraphs}\nJudge: ",
        )

        self.inference_template = PromptTemplate(
            config=config,
            system_prompt=GOLDEN_INFERENCE_SYSTEM_PROMPT,
            user_prompt="Query: {question}\nEvidence:\n{paragraphs}\nAnswer: ",
        )

        self.aggregate_template = PromptTemplate(
            config=config,
            system_prompt=GOLDEN_AGGREGATE_SYSTEM_PROMPT,
            user_prompt="Query: {question}\nEvidence:\n{paragraphs}\nAnswer: ",
        )

        self.date_template = PromptTemplate(
            config=config,
            system_prompt=DATE_FORMAT_SYSTEM_PROMPT,
            user_prompt="Input: {date}\nOutput: ",
        )

    def get_answers_with_golden(self, tid, query, supports):
        if self.dataset_name == "hotpotqa":
            supports2str = [f"{support[0]}: {' '.join(support[1])}" for support in supports]
            paragraphs = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(supports2str)])
            prompt = [self.relevant_template.get_string(question=query, paragraphs=paragraphs)]
            support_id = str2json(self.generator.generate(prompt)[0])["Response"]
            supports_ = [supports[support_id-1]]

        elif self.dataset_name == "2wikimultihopqa":
            if self.config["split"][0].split("_")[0] in ["t1", "t2", "t3"]:
                idx = int(tid.replace("Q", "")) - 1
                supports_ = [supports[idx]]
            elif self.config["split"][0].split("_")[0] in ["t9", "t10"]:
                supports2str = [f"{support[0]}: {' '.join(support[1])}" for support in supports]
                paragraphs = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(supports2str)])
                prompt = [self.relevant_template.get_string(question=query, paragraphs=paragraphs)]
                support_id = str2json(self.generator.generate(prompt)[0])["Response"]
                supports_ = [supports[support_id-1]]

        elif self.dataset_name == "musique":
            supports_ = [supports[tid]]

        supports_ = [{"title": support[0], "contents": support[1]} for support in supports_]
        supports2str = [f"{support['title']}: {' '.join(support['contents'])}" for support in supports_]
        paragraphs = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(supports2str)])

        prompt = [self.inference_template.get_string(question=query, paragraphs=paragraphs)]
        answers = str2json(self.generator.generate(prompt)[0])["Response"]
        return supports_, answers
    
    def execute(self, item):
        def get_mid2nid(intermediate_logs):
            mid2nid = {}
            for k, _ in intermediate_logs.items():
                k1, k2 = k.split("_")[0], k
                if k1 not in mid2nid.keys():
                    mid2nid[k1] = [k2]
                else:
                    mid2nid[k1].append(k2)
            return mid2nid

        def get_sample_nodes(path, graph, sample_nodes):
            for node in graph.nodes():
                graph.nodes[node]['name'] = node

            sample_nodes_ = []
            for sample in sample_nodes:
                subgraph = nx.DiGraph()
                combinations = list(itertools.combinations(sample, 2))
                for combination in combinations:
                    path_ = tuple([node.split("_")[0] for node in combination])
                    if path_ in path:
                        subgraph.add_edges_from([combination])
                for node in subgraph.nodes():
                    subgraph.nodes[node]['name'] = node
                matcher = DiGraphMatcher(graph, subgraph, node_match=lambda x, y: x['name'] == y['name'])
                is_save = matcher.subgraph_is_isomorphic()
                if is_save:
                    sample_nodes_.append(sample)

            return sample_nodes_
        
        def get_candidate_answer(question, candidate_graph):
            graph = nx.DiGraph()
            for nid, node in candidate_graph.items():
                graph.add_node(nid)
                for previous_nid in node["previous"]:
                    graph.add_edge(previous_nid, nid)

            zero_out_degree_nodes = [n for n in graph.nodes() if graph.out_degree(n) == 0]
            if len(zero_out_degree_nodes) == 1:
                candidate_answer = candidate_graph[zero_out_degree_nodes[0]]["answer"]
                return candidate_answer
            elif len(zero_out_degree_nodes) == 2:
                paragraphs = "\n".join([f"{idx+1}. {node['query']} >> {node['answer']}" for idx, node in enumerate(list(candidate_graph.values()))])
                prompt = [self.aggregate_template.get_string(question=question, paragraphs=paragraphs)]
                candidate_answer = str2json(self.generator.generate(prompt)[0])["Response"]
                return candidate_answer
            elif len(zero_out_degree_nodes) == 4:
                person_live = {}
                for nid, node in candidate_graph.items():

                    person = node["supports"][0]["title"]
                    prompt = [self.date_template.get_string(date=node["answer"])]
                    date = str2json(self.generator.generate(prompt)[0])["Response"]
                    if person not in person_live.keys():
                        person_live[person] = [date]
                    else:
                        person_live[person].append(date)

                person_longer = ""
                persin_longer_days = 0
                for person, dates in person_live.items():

                    start = datetime(int(dates[0][0]), int(dates[0][1]), int(dates[0][2]))
                    end = datetime(int(dates[1][0]), int(dates[1][1]), int(dates[1][2]))

                    if start > end:
                        start, end = end, start

                    delta_days = (end - start).total_seconds() / 86400
                    if delta_days > persin_longer_days:
                        person_longer = person
                        persin_longer_days = delta_days

                candidate_answer = person_longer
                return candidate_answer

        question, plan, supports = item.question, item.metadata["plan"], item.metadata["supporting_facts"]
        graph = nx.DiGraph()
        path = []
        intermediate_logs = {}

        for mid, meta in plan.items():
            template, tag = meta[0], meta[1]
            pattern = r"<A(\d+)>"
            placeholders = re.findall(pattern, template)
            suffix = 1

            for placeholder in placeholders:
                path.append((f"Q{placeholder}", f"Q{re.findall(pattern, tag)[0]}"))

            if len(placeholders) == 0:
                query = template
                supports_, answers = self.get_answers_with_golden(mid, query, supports)

                for answer in answers:
                    if not have_not_support_word(answer):
                        nid = f"{mid}_{suffix}"
                        intermediate_logs[nid] = {
                            "template": template,
                            "previous": [f"Q{p}" for p in placeholders],
                            "query": query,
                            "supports": supports_,
                            "tag": tag,
                            "answer": answer
                            }
                        graph.add_node(nid)
                        suffix += 1

            else:
                previous_info = []
                for placeholder in placeholders:
                    previous_info.append([[k, v["tag"], v["answer"]] for k, v in intermediate_logs.items() if k.split("_")[0] == f"Q{placeholder}"])

                combinations = itertools.product(*previous_info)
                combinations = [list(x) for x in combinations]

                for combination in combinations:

                    query = template
                    paddings = []
                    for _, placeholder, padding in combination:
                        query = query.replace(placeholder, padding)
                        paddings.append(padding)

                    supports_, answers = self.get_answers_with_golden(mid, query, supports)


                    for answer in answers:
                        if not have_not_support_word(answer):
                        
                            nid = f"{mid}_{suffix}"
                            intermediate_logs[nid] = {
                                "template": template,
                                "previous": [f"Q{p}" for p in placeholders],
                                "query": query,
                                "supports": supports_,
                                "tag": tag,
                                "answer": answer
                                }
                            graph.add_node(nid)
                            for previous_nid, _, _ in combination:
                                graph.add_edge(previous_nid, nid)

                            suffix += 1

        mid_lst = list(plan.keys())
        nid_lst = list(set([k.split("_")[0] for k in list(intermediate_logs.keys())]))

        candidate_graphs = []
        if len(mid_lst) != len(nid_lst) or len(mid_lst) == 0:
            have_candidate = "[NONE]"
        else:
            mid2nid = get_mid2nid(intermediate_logs)

            sample_nodes = list(mid2nid.values())
            sample_nodes = itertools.product(*sample_nodes)
            sample_nodes = [list(x) for x in sample_nodes]
            sample_nodes = get_sample_nodes(path, graph, sample_nodes)

            for sample in sample_nodes:
                nodes = {nid.split("_")[0]: intermediate_logs[nid] for nid in sample}
                candidate_graphs.append(nodes)

        if len(candidate_graphs) == 0:
            have_candidate = "[NONE]"
        elif len(candidate_graphs) == 1:
            have_candidate = "[SINGLE]"
        elif len(candidate_graphs) > 1:
            have_candidate = f"[MULTIPLE]__NUM_{len(candidate_graphs)}"

        item.update_output("have_candidate", have_candidate)

        candidate_answers = []
        for candidate_graph in candidate_graphs:
            candidate_answer = get_candidate_answer(question, candidate_graph)
            candidate_answers.append(candidate_answer)

        candidate_graphs = [[g, a] for g, a in zip(candidate_graphs, candidate_answers)]
        item.metadata["candidate_graphs"] = candidate_graphs


class QualityController:
    def __init__(self, config, generator):
        self.config = config
        self.generator = generator
        self.dataset_name = self.config["dataset_name"]
        self.split = self.config["split"]

        self.judge_template = PromptTemplate(
            config=config,
            system_prompt=EVALUATE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nGolden answer: {golden_answers}\nPredicted answer: {answer}\nOutput: ",
        )

    def check(self, item):
        def judge_alignment(item, candidate_graph):
            question, answer = item.question, candidate_graph[1]
            golden_answers = item.golden_answers

            if answer.lower() in [golden_answer.lower() for golden_answer in golden_answers]:
                return True

            prompt = [self.judge_template.get_string(question=question, golden_answers=golden_answers[:5], answer=answer)]
            is_align = str2json(self.generator.generate(prompt)[0])["Response"]
            is_align = is_align.lower() == "yes"
            if is_align:
                item.golden_answers.append(answer)

            return is_align
        
        def judge_leakage(item, candidate_graph):
            if self.config["split"][0].split("_")[0] not in ["t2", "t9", "t10"]:
                graph, answer = candidate_graph[0], candidate_graph[1]
                inter_answers = [node["answer"] for node in list(graph.values())[:-1]]
                golden_answers = item.golden_answers
                if (len(set(inter_answers) & set(golden_answers)) == 0) and (answer not in inter_answers) and (len(inter_answers) == len(set(inter_answers))):
                    return False
                else:
                    return True
            else:
                return False
            
        final_graphs = []
        have_leakage = []
        candidate_graphs = item.metadata["candidate_graphs"]
        if len(candidate_graphs) != 0:
            for candidate_graph in candidate_graphs:
                is_leakage = judge_leakage(item, candidate_graph)
                have_leakage.append(is_leakage)
                if not is_leakage:
                    is_align = judge_alignment(item, candidate_graph)
                    if is_align:
                        final_graphs.append(candidate_graph)

        if len(final_graphs) == 0:
            if len(candidate_graphs) == 0:
                item.update_output("have_final", f"[NONE]__CANDIDATE_False")
            else:
                have_leakage = (sum(have_leakage) > 0) and (len(final_graphs) == 0)
                item.update_output("have_final", f"[NONE]__LEAKAGE_{have_leakage}")
            item.update_output("pred", "[INFERENCE_ERROR]")
        else:
            if len(final_graphs) == 1:
                item.update_output("have_final", "[SINGLE]")
            else:
                item.update_output("have_final",f"[MULTIPLE]__NUM_{len(final_graphs)}")
            item.update_output("pred", final_graphs[0][1])

        item.golden_answers = list(set(item.golden_answers))
        item.update_output("final_graphs", final_graphs)


class PERQAPlanner:
    def __init__(self, config):
        config = Config(config_dict=openai_config_dict, is_components=True)
        self.generator = get_generator(config)
        self.config = config

    def get_type(self, question):
        template = PromptTemplate(
            config=self.config,
            system_prompt=TYPE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nOutput: ",
        )

        prompt = [template.get_string(question=question)]
        question_type = self.generator.generate(prompt)[0]
        question_type = str2json(question_type)["Response"]
        return question_type

    def get_bridge_plan(self, question):
        template = PromptTemplate(
            config=self.config,
            system_prompt=BRIDGE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nResult: ",
        )

        prompt = [template.get_string(question=question)]
        predicted_plan = self.generator.generate(prompt)[0]
        predicted_plan = str2json(predicted_plan)["Response"]

        return predicted_plan
    
    def get_comparison_plan(self, question):
        template = PromptTemplate(
            config=self.config,
            system_prompt=COMPARISON_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nResult: ",
        )

        prompt = [template.get_string(question=question)]
        predicted_plan = self.generator.generate(prompt)[0]
        predicted_plan = str2json(predicted_plan)["Response"]

        return predicted_plan
    
    def run(self, item):
        question = item.question
        question_type = self.get_type(question)
        if question_type.lower() == "bridge":
            predicted_plan = self.get_bridge_plan(question)
        elif question_type.lower() == "comparison":
            predicted_plan = self.get_comparison_plan(question)

        item.update_output("type", question_type)
        item.update_output("predicted_plan", predicted_plan)

        return predicted_plan


class PERQAExecutor:
    def __init__(self, config, retriever, generator):
        self.config = config
        self.retriever = retriever
        self.generator = generator
        self.dataset_name = self.config["dataset_name"]
        self.split = self.config["split"]

        self.aggregate_template = None

    def get_answers_with_or_without_retrieval(self, query):
        pass

    def set_bridge_aggregate_template(self):
        self.aggregate_template = PromptTemplate(
            config=self.config,
            system_prompt=BRIDGE_AGGREGATE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nEvidence:\n{paragraphs}\nAnswer: ",
        )

    def set_comparison_aggregate_template(self):
        self.aggregate_template = PromptTemplate(
            config=self.config,
            system_prompt=COMPARISON_AGGREGATE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nEvidence:\n{paragraphs}\nAnswer: ",
        )

    def execute(self, item, plan):
        pass

    def aggregate(self, item, candidate_graphs):
        if item.output["type"].lower() == "bridge":
            self.set_bridge_aggregate_template()
        elif item.output["type"].lower() == "comparison":
            self.set_comparison_aggregate_template()

        final_graphs_ = []
        if len(candidate_graphs) != 0:
            question = item.question
            final_graphs = []
            for candidate_graph in candidate_graphs:
                evidence2str = [f"{v['query']} >> {v['answer']}" for _, v in candidate_graph.items()]
                paragraphs = "\n".join([f"{cno + 1}. {context}" for cno, context in enumerate(evidence2str)])

                prompt = [self.aggregate_template.get_string(question=question, paragraphs=paragraphs)]
                final_answer = str2json(self.generator.generate(prompt)[0])["Response"]

                final_graphs.append([candidate_graph, final_answer])

            final_answers = [final_answer for _, final_answer in final_graphs]
            final_answer_counts = {answer: final_answers.count(answer) for answer in set(final_answers)}
            max_count = max(final_answer_counts.values())
            final_answers_with_max_count = [answer for answer, count in final_answer_counts.items() if
                                            count == max_count]
            final_answers = final_answers_with_max_count

            final_graphs_ = [final_graph for final_graph in final_graphs if final_graph[1] in final_answers]

        item.update_output("final_graphs", final_graphs_)

        return final_graphs_

    def run(self, item, plan):
        pass


class PERQAChatExecutor(PERQAExecutor):
    def __init__(self, config, retriever, generator):
        super().__init__(config, retriever, generator)

        self.aggregate_template = PromptTemplate(
            config=config,
            system_prompt=MHQA_AGGREGATE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nEvidence:\n{paragraphs}\nAnswer: ",
        )

        self.inference_without_retrieve_template = PromptTemplate(
            config=config,
            system_prompt=VANILLA_QA_SYSTEM_PROMPT,
            user_prompt="Query: {question}\nAnswer: ",
        )

    def get_answers_with_or_without_retrieval(self, query):
        retrievals = []
        prompt = [self.inference_without_retrieve_template.get_string(question=query)]
        answers = str2json(self.generator.generate(prompt)[0])["Response"]

        if isinstance(answers, str):
            answers = [answers]

        return retrievals, answers

    def execute(self, item, plan):
        def get_support_answers(answers):
            not_support_words = ["unknown", "support", "describe", "unclear", "insufficient", "unspecified", "mention",
                                 "evidence", "undefined", "none", "available", "information", "found"]
            support_answers = []
            for answer in answers:
                if any(ns_word in answer.lower() for ns_word in ["[]", "[ ]", "not ", "there is no"]):
                    continue
                answer_words = re.split(r'[\s,.?!]+', answer)
                if any(ans_word.lower() in not_support_words for ans_word in answer_words):
                    continue
                if "no " in answer.lower() and " no " not in answer.lower():
                    continue
                support_answers.append(answer)

            return support_answers

        def get_mid2nid(intermediate_logs):
            mid2nid = {}
            for k, _ in intermediate_logs.items():
                k1, k2 = k.split("_")[0], k
                if k1 not in mid2nid.keys():
                    mid2nid[k1] = [k2]
                else:
                    mid2nid[k1].append(k2)
            return mid2nid

        def get_sample_nodes(path, graph, sample_nodes):

            for node in graph.nodes():
                graph.nodes[node]['name'] = node

            sample_nodes_ = []
            for sample in sample_nodes:
                subgraph = nx.DiGraph()
                combinations = list(itertools.combinations(sample, 2))
                for combination in combinations:
                    path_ = tuple([node.split("_")[0] for node in combination])
                    if path_ in path:
                        subgraph.add_edges_from([combination])
                for node in subgraph.nodes():
                    subgraph.nodes[node]['name'] = node
                matcher = DiGraphMatcher(graph, subgraph, node_match=lambda x, y: x['name'] == y['name'])
                is_save = matcher.subgraph_is_isomorphic()
                if is_save:
                    sample_nodes_.append(sample)

            return sample_nodes_

        graph = nx.DiGraph()
        path = []
        intermediate_logs = {}

        for mid, meta in plan.items():

            template, tag = meta[0], meta[1]
            pattern = r"<A(\d+)>"
            placeholders = re.findall(pattern, template)
            suffix = 1

            for placeholder in placeholders:
                path.append((f"Q{placeholder}", f"Q{re.findall(pattern, tag)[0]}"))

            if len(placeholders) == 0:
                query = template
                supports, answers = self.get_answers_with_or_without_retrieval(query)
                answers = get_support_answers(answers)

                if len(answers) != 0:
                    for answer in answers:
                        nid = f"{mid}_{suffix}"
                        intermediate_logs[nid] = {
                            "template": template,
                            "previous": [f"Q{p}" for p in placeholders],
                            "query": query,
                            "supports": supports,
                            "tag": tag,
                            "answer": answer
                        }
                        graph.add_node(nid)
                        suffix += 1
                else:
                    nid = f"{mid}_{suffix}"
                    intermediate_logs[nid] = {
                        "template": template,
                        "previous": [f"Q{p}" for p in placeholders],
                        "query": query,
                        "supports": supports,
                        "tag": tag,
                        "answer": "[Not support]"
                    }
                    suffix += 1

            else:
                previous_info = []
                for placeholder in placeholders:
                    previous_info.append([[k, v["tag"], v["answer"]] for k, v in intermediate_logs.items() if
                                          k.split("_")[0] == f"Q{placeholder}" and v["answer"] != "[Not support]"])
                if len(previous_info) != len(placeholders):
                    break
                combinations = itertools.product(*previous_info)
                combinations = [list(x) for x in combinations]
                for combination in combinations:
                    query = template
                    paddings = []
                    for _, placeholder, padding in combination:
                        query = query.replace(placeholder, padding)
                        paddings.append(padding)

                    supports, answers = self.get_answers_with_or_without_retrieval(query)
                    answers = get_support_answers(answers)

                    if len(answers) != 0:
                        for answer in answers:
                            nid = f"{mid}_{suffix}"
                            intermediate_logs[nid] = {
                                "template": template,
                                "previous": [f"Q{p}" for p in placeholders],
                                "query": query,
                                "supports": supports,
                                "tag": tag,
                                "answer": answer
                            }
                            graph.add_node(nid)
                            for previous_nid, _, _ in combination:
                                graph.add_edge(previous_nid, nid)
                            suffix += 1
                    else:
                        nid = f"{mid}_{suffix}"
                        intermediate_logs[nid] = {
                            "template": template,
                            "previous": [f"Q{p}" for p in placeholders],
                            "query": query,
                            "supports": supports,
                            "tag": tag,
                            "answer": "[Not support]"
                        }
                        suffix += 1

        intermediate_logs_without_not_support = {k: v for k, v in intermediate_logs.items() if
                                                 v["answer"] != "[Not support]"}

        mid_lst = list(plan.keys())
        nid_lst = list(set([k.split("_")[0] for k in intermediate_logs_without_not_support.keys()]))
        mid2nid = get_mid2nid(intermediate_logs_without_not_support)

        sample_nodes = list(mid2nid.values())
        sample_nodes = itertools.product(*sample_nodes)
        sample_nodes = [list(x) for x in sample_nodes]
        sample_nodes = get_sample_nodes(path, graph, sample_nodes)

        candidate_graphs = []
        incomplete_graphs = []
        have_candidate = "[NONE]"
        if not (len(mid_lst) != len(nid_lst) or len(mid_lst) == 0):
            for sample in sample_nodes:
                nodes = {nid.split("_")[0]: intermediate_logs[nid] for nid in sample}
                candidate_graphs.append(nodes)

        if len(candidate_graphs) == 0:
            if len(intermediate_logs_without_not_support) != 0:
                have_candidate = "[INCOMPLETE]"
                for sample in sample_nodes:
                    nodes = {nid.split("_")[0]: intermediate_logs[nid] for nid in sample}
                    incomplete_graphs.append(nodes)

        elif len(candidate_graphs) == 1:
            have_candidate = "[SINGLE]"
        elif len(candidate_graphs) > 1:
            have_candidate = f"[MULTIPLE]__NUM_{len(candidate_graphs)}"

        item.update_output("have_candidate", have_candidate)
        item.update_output("incomplete_graphs", incomplete_graphs)
        item.update_output("candidate_graphs", candidate_graphs)

        return incomplete_graphs, candidate_graphs

    def run(self, item, plan):
        incomplete_graphs, candidate_graphs = self.execute(item, plan)
        final_graphs = self.aggregate(item, candidate_graphs)

        return incomplete_graphs, final_graphs


class PERQARAGExecutor(PERQAExecutor):
    def __init__(self, config, retriever, generator):
        super().__init__(config, retriever, generator)

        self.relevant_template = PromptTemplate(
            config=config,
            system_prompt=MHQA_RELEVANT_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nRetrievals:\n{paragraphs}\nJudge: ",
        )

        self.rewrite_template = PromptTemplate(
            config=config,
            system_prompt=MHQA_REWRITE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nAnswer: ",
        )

        self.hyde_template = PromptTemplate(
            config=config,
            system_prompt=HYDE_SYSTEM_PROMPT,
            user_prompt="Question: {question}\nPassage: ",
        )

        self.inference_template = PromptTemplate(
            config=config,
            system_prompt=RAG_QA_SYSTEM_PROMPT,
            user_prompt="Query: {question}\nRetrievals:\n{paragraphs}\nAnswer: ",
        )

        self.use_relevant_expert = self.config["multihopqa_params"]["use_relevant_expert"]
        self.use_rewriter = self.config["multihopqa_params"]["use_rewriter"]
        self.use_hyde = self.config["multihopqa_params"]["use_hyde"]

    def get_relevant_retrieval_id(self, query, retrievals):
        retrievals2str = [f"{retrieval['title']}: {retrieval['contents']}" for retrieval in retrievals]
        paragraphs = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(retrievals2str)])

        prompt = [self.relevant_template.get_string(question=query, paragraphs=paragraphs)]
        result = self.generator.generate(prompt)[0]

        try:
            relevant_id = str2json(result)["Response"]
        except TypeError:
            relevant_id = []

        return relevant_id

    def get_rewrite_query(self, query):
        prompt = [self.rewrite_template.get_string(question=query)]
        keyword = str2json(self.generator.generate(prompt)[0])["Response"]
        rewrite_query = query + " " + keyword
        print(f"rewrite_query: {rewrite_query}")
        return rewrite_query
    
    def get_hyde_query(self, query):
        prompt = [self.hyde_template.get_string(question=query)]
        hyde_query = self.generator.generate(prompt)[0].split("\n")[0]
        hyde_query = " ".join([query for _ in range(5)]) + " " + hyde_query
        print(f"hyde_query: {hyde_query}")
        return hyde_query
    
    def get_answers_with_or_without_retrieval(self, query, retrieve_query=None):
        if retrieve_query is None:
            retrieve_query = query

        retrievals = self.retriever.search(retrieve_query)
        retrievals = [retrieval["contents"].split("\n") for retrieval in retrievals]
        retrievals = [{"title": retrieval[0][1:-1], "contents": " ".join(retrieval[1:])} for retrieval in retrievals]

        if self.use_relevant_expert:
            relevant_id = self.get_relevant_retrieval_id(query, retrievals)
            retrievals = [retrievals[i-1] for i in relevant_id]

        if len(retrievals) == 0:
            return [], ["Not support"]
        
        retrievals2str = [f"{retrieval['title']}: {retrieval['contents']}" for retrieval in retrievals]
        paragraphs = "\n".join([f"{cno+1}. {context}" for cno, context in enumerate(retrievals2str)])

        # QA with Retrievals
        prompt = [self.inference_template.get_string(question=query, paragraphs=paragraphs)]
        answers = str2json(self.generator.generate(prompt)[0])["Response"]

        if isinstance(answers, str):
            answers = [answers]

        return retrievals, answers
    
    def execute(self, item, plan, max_answer_num=1):
        def get_support_answers(answers):
            not_support_words = ["unknown", "support", "describe", "unclear", "insufficient", "unspecified", "mention", "evidence", "undefined", "none", "available", "information", "found"]
            support_answers = []
            for answer in answers:
                if any(ns_word in answer.lower() for ns_word in ["[]", "[ ]", "not ", "there is no"]):
                    continue
                answer_words = re.split(r'[\s,.?!]+', answer)
                if any(ans_word.lower() in not_support_words for ans_word in answer_words):
                    continue
                if "no " in answer.lower() and " no " not in answer.lower():
                    continue
                support_answers.append(answer)
            
            return support_answers

        def get_mid2nid(intermediate_logs):
            mid2nid = {}
            for k, _ in intermediate_logs.items():
                k1, k2 = k.split("_")[0], k
                if k1 not in mid2nid.keys():
                    mid2nid[k1] = [k2]
                else:
                    mid2nid[k1].append(k2)
            return mid2nid

        def get_sample_nodes(path, graph, sample_nodes):
            for node in graph.nodes():
                graph.nodes[node]['name'] = node

            sample_nodes_ = []
            for sample in sample_nodes:
                subgraph = nx.DiGraph()
                combinations = list(itertools.combinations(sample, 2))
                for combination in combinations:
                    path_ = tuple([node.split("_")[0] for node in combination])
                    if path_ in path:
                        subgraph.add_edges_from([combination])
                for node in subgraph.nodes():
                    subgraph.nodes[node]['name'] = node
                matcher = DiGraphMatcher(graph, subgraph, node_match=lambda x, y: x['name'] == y['name'])
                is_save = matcher.subgraph_is_isomorphic()
                if is_save:
                    sample_nodes_.append(sample)

            return sample_nodes_
        
        graph = nx.DiGraph()
        path = []
        intermediate_logs = {}

        for mid, meta in plan.items():

            template, tag = meta[0], meta[1]
            pattern = r"<A(\d+)>"
            placeholders = re.findall(pattern, template)
            suffix = 1

            for placeholder in placeholders:
                path.append((f"Q{placeholder}", f"Q{re.findall(pattern, tag)[0]}"))

            if len(placeholders) == 0:
                query = template

                is_break = False
                if self.use_hyde:
                    rewrite_query = self.get_hyde_query(query)
                    is_break = True
                else:
                    rewrite_query = None

                while True:
                    try:
                        supports, answers = self.get_answers_with_or_without_retrieval(query, rewrite_query)
                        answers = get_support_answers(answers)
                        answers = answers[:max_answer_num]
                    except:
                        answers = []
                    if len(answers) != 0:
                        for answer in answers:  
                            nid = f"{mid}_{suffix}"
                            intermediate_logs[nid] = {
                                "template": template,
                                "previous": [f"Q{p}" for p in placeholders],
                                "query": query,
                                "rewrite_query": rewrite_query,
                                "supports": supports,
                                "tag": tag,
                                "answer": answer
                                }
                            graph.add_node(nid)
                            suffix += 1
                        break
                    else:
                        if is_break or not self.use_rewriter:
                            nid = f"{mid}_{suffix}"
                            intermediate_logs[nid] = {
                                "template": template,
                                "previous": [f"Q{p}" for p in placeholders],
                                "query": query,
                                "rewrite_query": rewrite_query,
                                "supports": supports,
                                "tag": tag,
                                "answer": "[Not support]"
                                }
                            suffix += 1
                            break
                        rewrite_query = self.get_rewrite_query(query)
                        is_break = True
                        
            else:
                previous_info = []
                for placeholder in placeholders:
                    previous_info.append([[k, v["tag"], v["answer"]] for k, v in intermediate_logs.items() if k.split("_")[0] == f"Q{placeholder}" and v["answer"] != "[Not support]"])
                if len(previous_info) != len(placeholders):
                    break
                combinations = itertools.product(*previous_info)
                combinations = [list(x) for x in combinations]
                for combination in combinations:
                    query = template
                    paddings = []
                    for _, placeholder, padding in combination:
                        query = query.replace(placeholder, padding)
                        paddings.append(padding)

                    is_break = False
                    if self.use_hyde:
                        rewrite_query = self.get_hyde_query(query)
                        is_break = True
                    else:
                        rewrite_query = None

                    while True:
                        try:
                            supports, answers = self.get_answers_with_or_without_retrieval(query, rewrite_query)
                            answers = get_support_answers(answers)
                            answers = answers[:max_answer_num]
                        except:
                            answers = []
                        if len(answers) != 0:
                            for answer in answers:  
                                nid = f"{mid}_{suffix}"
                                intermediate_logs[nid] = {
                                    "template": template,
                                    "previous": [f"Q{p}" for p in placeholders],
                                    "query": query,
                                    "rewrite_query": rewrite_query,
                                    "supports": supports,
                                    "tag": tag,
                                    "answer": answer
                                    }
                                graph.add_node(nid)
                                for previous_nid, _, _ in combination:
                                    graph.add_edge(previous_nid, nid)
                                suffix += 1
                            break
                        else:
                            if is_break or not self.use_rewriter:
                                nid = f"{mid}_{suffix}"
                                intermediate_logs[nid] = {
                                    "template": template,
                                    "previous": [f"Q{p}" for p in placeholders],
                                    "query": query,
                                    "rewrite_query": rewrite_query,
                                    "supports": supports,
                                    "tag": tag,
                                    "answer": "[Not support]"
                                    }
                                suffix += 1
                                break
                            rewrite_query = self.get_rewrite_query(query)
                            is_break = True

        intermediate_logs_without_not_support = {k: v for k, v in intermediate_logs.items() if v["answer"] != "[Not support]"}

        mid_lst = list(plan.keys())
        nid_lst = list(set([k.split("_")[0] for k in intermediate_logs_without_not_support.keys()]))
        mid2nid = get_mid2nid(intermediate_logs_without_not_support)

        sample_nodes = list(mid2nid.values())
        sample_nodes = itertools.product(*sample_nodes)
        sample_nodes = [list(x) for x in sample_nodes]
        sample_nodes = get_sample_nodes(path, graph, sample_nodes)


        candidate_graphs = []
        incomplete_graphs = []
        have_candidate = "[NONE]"
        if not (len(mid_lst) != len(nid_lst) or len(mid_lst) == 0):
            for sample in sample_nodes:
                nodes = {nid.split("_")[0]: intermediate_logs[nid] for nid in sample}
                candidate_graphs.append(nodes)

        if len(candidate_graphs) == 0:
            if len(intermediate_logs_without_not_support) != 0:
                have_candidate = "[INCOMPLETE]"
                for sample in sample_nodes:
                    nodes = {nid.split("_")[0]: intermediate_logs[nid] for nid in sample}
                    incomplete_graphs.append(nodes)

        elif len(candidate_graphs) == 1:
            have_candidate = "[SINGLE]"
        elif len(candidate_graphs) > 1:
            have_candidate = f"[MULTIPLE]__NUM_{len(candidate_graphs)}"

        item.update_output("have_candidate", have_candidate)
        item.update_output("incomplete_graphs", incomplete_graphs)
        item.update_output("candidate_graphs", candidate_graphs)
        
        return incomplete_graphs, candidate_graphs

    def run(self, item, plan):
        incomplete_graphs, candidate_graphs = self.execute(item, plan)
        final_graphs = self.aggregate(item, candidate_graphs)

        return incomplete_graphs, final_graphs