from flashrag.config import Config
from flashrag.utils import get_dataset, run_pipeline
from flashrag.utils.utils import str2json
from prompt import RAG_MHQA_SYSTEM_PROMPT, VANILLA_QA_SYSTEM_PROMPT


def per_dp(config_dict):
    from pipeline import DatasetPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 1024,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 5000

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict["split"]]

    pipeline = DatasetPipeline(config)
    run_pipeline(config, pipeline, test_data)


def per_qa_chat(config_dict):
    from pipeline import PERQAChatPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 1024,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 5000

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict["split"]]

    pipeline = PERQAChatPipeline(config)
    run_pipeline(config, pipeline, test_data)


def per_qa_rag(config_dict):
    from pipeline import PERQARAGPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 1024,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 5000

    multihopqa_params = {
        "use_relevant_expert": False,
        "use_rewriter": False,
        "use_hyde": True
    }
    config_dict["multihopqa_params"] = multihopqa_params

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict["split"]]

    pipeline = PERQARAGPipeline(config)
    run_pipeline(config, pipeline, test_data)


def zeroshot(config_dict):
    from flashrag.prompt import PromptTemplate
    from pipeline import ZeroShotPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 1024,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 5000

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict['split']]

    template = PromptTemplate(
        config=config,
        system_prompt=VANILLA_QA_SYSTEM_PROMPT,
        user_prompt="Question: {question}\nAnswer: ",
    )

    def output2str(x):
        try:
            result = str2json(x)["Response"]
            return result
        except:
            return "[SYSTEM_ERROR]"

    pred_process_fun = lambda x: output2str(x)
    pipeline = ZeroShotPipeline(config, template)
    run_pipeline(config, pipeline, test_data, pred_process_fun)


def naiverag(config_dict):
    from flashrag.prompt import PromptTemplate
    from pipeline import NaiveRAGPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 1024,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 5000

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict['split']]

    template = PromptTemplate(
        config=config,
        system_prompt=RAG_MHQA_SYSTEM_PROMPT,
        user_prompt="Query: {question}\nRetrievals:\n{paragraphs}\nAnswer: ",
    )

    def output2str(x):
        try:
            result = str2json(x)["Response"]
            return result
        except:
            return "[SYSTEM_ERROR]"

    pred_process_fun = lambda x: output2str(x)
    pipeline = NaiveRAGPipeline(config, template)
    run_pipeline(config, pipeline, test_data, pred_process_fun)


def selfask(config_dict):
    from flashrag.pipeline import SelfAskPipeline

    generation_params = {
        "do_sample": False,
        "max_tokens": 256,
        "temperature": 0.0
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 10000

    selfask_params = {
        "max_iter": 6,
        "single_hop": False,
        "follow_up_pattern": r"Follow up:.*\n"
    }

    config_dict["selfask_params"] = selfask_params

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict['split']]

    pipeline = SelfAskPipeline(config)
    run_pipeline(config, pipeline, test_data)


def ircot(config_dict):
    from flashrag.pipeline import IRCOTPipeline

    generation_params = {
        "do_sample": False,
        "temperature": 0.0,
    }
    config_dict["generation_params"] = generation_params
    config_dict["generator_max_input_len"] = 10000

    config = Config(config_dict=config_dict)
    all_split = get_dataset(config)
    test_data = all_split[config_dict["split"]]

    pipeline = IRCOTPipeline(config, max_iter=15)
    
    run_pipeline(config, pipeline, test_data)

