import os
import json
import time
from tqdm import tqdm


from flashrag.config.config import Config
from flashrag.dataset.dataset import Dataset, Item
from flashrag.evaluator.metrics import ExactMatch, F1_Score
from flashrag.pipeline import BasicPipeline
from flashrag.utils import get_retriever, get_generator, print_now, set_logger

from module import PERQARAGExecutor, PERQAChatExecutor, PERDPPlanner, PERDPExecutor, PERQAPlanner, QualityController
from evaluate import Plan_Score, Step_Score


openai_config_dict = {
    # Generator Settings
    "framework": "openai",
    "generator_model": "gpt-4o-mini-2024-07-18",
    "generator_max_input_len": 5000,
    "generator_batch_size": 4,
    "generation_params": {
        "do_sample": False,
        "temperature": 1.0,
        "max_tokens": 1024
    },

    "openai_setting": {
        "base_url": "YOUR_URL",
        "api_key": "YOUR_KEY"
    }
}


class DatasetPipeline(BasicPipeline):
    def __init__(
        self,
        config,
        prompt_template=None,
        generator=None,
    ):
        super().__init__(config, prompt_template)

        self.config = config
        self.generator = get_generator(config) if generator is None else generator

        self.plan_completor = PERDPPlanner(self.config, self.generator)
        self.plan_executor = PERDPExecutor(self.config, self.generator)
        self.quality_controller = QualityController(self.config, self.generator)

        self.continue_evaluator = ExactMatch(config)

    def run_item(self, item):
        self.plan_completor.complete(item)
        self.plan_executor.execute(item)
        self.quality_controller.check(item)

    def run(self, dataset, do_eval=True):
        iter_num = 1
        iter_max_num = 5
        drop_ratios = []
        while True:
            start = time.time()
            if iter_num == 1:
                for item in tqdm(dataset, desc="Inference: "):
                    try:
                        self.run_item(item)
                    except Exception as e:
                        print(e)
                        item.update_output("pred", "[SYSTEM_ERROR]")

            else:
                config = Config(config_dict=openai_config_dict, is_components=True)
                generator_ = get_generator(config)

                self.plan_completor = PERDPPlanner(self.config, generator_)
                self.plan_executor = PERDPExecutor(self.config, generator_)
                self.quality_controller = QualityController(self.config, generator_)

                with open(f"{self.config['save_dir']}/intermediate_data_{iter_num-1}.json", "r") as f:
                    data = json.load(f)

                data = [Item(d) for d in data]
                dataset = Dataset(data=data)
                for item in tqdm(dataset, desc="Inference: "):
                    if self.continue_evaluator.calculate_em(item.pred, item.golden_answers) != 1.0:
                        try:
                            self.run_item(item)
                        except Exception as e:
                            print(e)
                            item.update_output("pred", "[SYSTEM_ERROR]")


            _, drop_ratio = self.evaluate(dataset, do_eval=do_eval, save_file_name=f"intermediate_data_{iter_num}.json")
            drop_ratio = round(1 - drop_ratio["em"], 4)
            drop_ratios.append(drop_ratio)
            end = time.time()
            set_logger(self.config, info=[f"[{print_now(1)}] iter_{iter_num}_drop_ratio: {drop_ratio}, time cost: {round(end - start, 4)} s"])

            iter_num += 1
            
            if iter_num > iter_max_num or drop_ratio == 0.0:
                break

        return dataset
    

class PERQAChatPipeline(BasicPipeline):
    def __init__(
        self,
        config,
        prompt_template=None,
        retriever=None,
        generator=None,
    ):

        super().__init__(config, prompt_template)

        self.config = config
        self.save_dir = config["save_dir"]

        self.retriever = get_retriever(config) if retriever is None else retriever
        self.generator = get_generator(config) if generator is None else generator

        self.planner = PERQAPlanner(self.config)
        self.executor = PERQAChatExecutor(self.config, self.retriever, self.generator)

        self.f1_evaluator = F1_Score(self.config)
        self.plan_evaluator = Plan_Score(self.config)
        self.step_evaluator = Step_Score(self.config)

    def calculate_final_score(self, plan_score, step_score):
        return (2 * plan_score * step_score) / (plan_score + step_score + 1e-6)
    
    def update_metric_score(self, item, predicted_plan, final_graphs, incomplete_graphs):
        metric_score = {}
        if len(final_graphs) != 0:
            f1_score = [self.f1_evaluator.token_level_scores(final_answer, item.golden_answers)["f1"] for _, final_answer in final_graphs]
            f1_score = sum(f1_score) / len(f1_score)
        else:
            f1_score = 0.0

        mapping, plan_scores = self.plan_evaluator.calculate_plan_score(predicted_plan, item.metadata["plan"])
        step_score = self.step_evaluator.calculate_step_score(final_graphs, incomplete_graphs, item.metadata["graph"], mapping)
        pse_g_score = self.calculate_final_score(plan_scores["plan_score"], step_score["step_score"])

        metric_score.update({"f1": f1_score, "pse_g": pse_g_score})
        metric_score.update(plan_scores)
        metric_score.update(step_score)

        item.update_output("mapping", mapping)
        item.update_output("metric_score", metric_score)

        return f1_score, pse_g_score

    def run_item(self, item):

        predicted_plan = self.planner.run(item)
        incomplete_graphs, final_graphs = self.executor.run(item, predicted_plan)

        f1_score, pse_g_score = self.update_metric_score(item, predicted_plan, final_graphs, incomplete_graphs)
        return f1_score, pse_g_score

    def run(self, dataset, pred_process_fun=None):
        
        final_f1_score, final_pse_g_score = [], []
        for item in tqdm(dataset, desc="Inference: "):
            try:
                f1_score, pse_g_score = self.run_item(item)
                final_f1_score.append(f1_score)
                final_pse_g_score.append(pse_g_score)

            except Exception as e:
                print(e)
                item.update_output("pred", "[SYSTEM_ERROR]")

        save_path = os.path.join(self.save_dir, "intermediate_data.json")
        dataset.save(save_path)

        set_logger(self.config, info=[f"final_f1_score: {sum(final_f1_score) / len(dataset)}", f"final_pse_g_score: {sum(final_pse_g_score) / len(dataset)}"])

        return dataset
    

class PERQARAGPipeline(BasicPipeline):
    def __init__(
        self,
        config,
        prompt_template=None,
        retriever=None,
        generator=None,
    ):

        super().__init__(config, prompt_template)

        self.config = config
        self.save_dir = config["save_dir"]

        self.retriever = get_retriever(config) if retriever is None else retriever
        self.generator = get_generator(config) if generator is None else generator

        self.planner = PERQAPlanner(self.config)
        self.executor = PERQARAGExecutor(self.config, self.retriever, self.generator)

        self.f1_evaluator = F1_Score(self.config)
        self.plan_evaluator = Plan_Score(self.config)
        self.step_evaluator = Step_Score(self.config)

    def calculate_final_score(self, plan_score, step_score):
        return (2 * plan_score * step_score) / (plan_score + step_score + 1e-6)
    
    def update_metric_score(self, item, predicted_plan, final_graphs, incomplete_graphs):
        metric_score = {}
        if len(final_graphs) != 0:
            f1_score = [self.f1_evaluator.token_level_scores(final_answer, item.golden_answers)["f1"] for _, final_answer in final_graphs]
            f1_score = sum(f1_score) / len(f1_score)
        else:
            f1_score = 0.0

        mapping, plan_scores = self.plan_evaluator.calculate_plan_score(predicted_plan, item.metadata["plan"])
        step_score = self.step_evaluator.calculate_step_score(final_graphs, incomplete_graphs, item.metadata["graph"], mapping)
        pse_g_score = self.calculate_final_score(plan_scores["plan_score"], step_score["step_score"])

        metric_score.update({"f1": f1_score, "pse_g": pse_g_score})
        metric_score.update(plan_scores)
        metric_score.update(step_score)

        item.update_output("mapping", mapping)
        item.update_output("metric_score", metric_score)

        return f1_score, pse_g_score

    def run_item(self, item):
        predicted_plan = self.planner.run(item)
        incomplete_graphs, final_graphs = self.executor.run(item, predicted_plan)

        f1_score, pse_g_score = self.update_metric_score(item, predicted_plan, final_graphs, incomplete_graphs)
        return f1_score, pse_g_score

    def run(self, dataset, pred_process_fun=None):
        final_f1_score, final_pse_g_score = [], []
        for item in tqdm(dataset, desc="Inference: "):
            try:
                f1_score, pse_g_score = self.run_item(item)
                final_f1_score.append(f1_score)
                final_pse_g_score.append(pse_g_score)

            except Exception as e:
                print(e)
                item.update_output("pred", "[SYSTEM_ERROR]")
        

        save_path = os.path.join(self.save_dir, "intermediate_data.json")
        dataset.save(save_path)

        set_logger(self.config, info=[f"final_f1_score: {sum(final_f1_score) / len(dataset)}", f"final_pse_g_score: {sum(final_pse_g_score) / len(dataset)}"])

        return dataset


class ZeroShotPipeline(BasicPipeline):
    def __init__(self, config, prompt_template=None, generator=None):
        """
        inference stage:
            query -> generator
        """

        super().__init__(config, prompt_template)
        if generator is None:
            self.generator = get_generator(config)
        else:
            self.generator = generator

    def run(self, dataset, do_eval=True, pred_process_fun=None):

        input_prompts = [self.prompt_template.get_string(question=q) for q in dataset.question]
        dataset.update_output("prompt", input_prompts)

        pred_answers_list = self.generator.generate(input_prompts)
        dataset.update_output("pred", pred_answers_list)

        dataset, eval_result = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        print(eval_result)
        return dataset


class NaiveRAGPipeline(BasicPipeline):
    def __init__(self, config, prompt_template=None, retriever=None, generator=None):
        """
        inference stage:
            query -> generator
        """

        super().__init__(config, prompt_template)
        self.retriever = get_retriever(config) if retriever is None else retriever
        self.generator = get_generator(config) if generator is None else generator

    def run(self, dataset, do_eval=True, pred_process_fun=None):
        input_query = dataset.question

        retrievals_all = self.retriever.batch_search(input_query)
        retrievals_all_ = []
        paragraphs_all = []
        for retrievals in retrievals_all:
            retrievals = [retrieval["contents"].split("\n") for retrieval in retrievals]
            retrievals = [{"title": retrieval[0][1:-1], "contents": " ".join(retrieval[1:])} for retrieval in
                          retrievals]
            retrievals_all_.append(retrievals)

            retrievals2str = [f"{retrieval['title']}: {retrieval['contents']}" for retrieval in retrievals]
            paragraphs = "\n".join([f"{cno + 1}. {context}" for cno, context in enumerate(retrievals2str)])
            paragraphs_all.append(paragraphs)

        dataset.update_output("retrieval_result", retrievals_all_)
        input_prompts = [
            self.prompt_template.get_string(question=q, paragraphs=r)
            for q, r in zip(dataset.question, paragraphs_all)
        ]
        dataset.update_output("prompt", input_prompts)

        pred_answers_list = self.generator.generate(input_prompts)
        dataset.update_output("pred", pred_answers_list)

        dataset, eval_result = self.evaluate(dataset, do_eval=do_eval, pred_process_fun=pred_process_fun)
        print(eval_result)
        return dataset