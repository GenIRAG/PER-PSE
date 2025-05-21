This project is forked and modified from the open source project FlashRAG.

To run this project: 

1. Add relevant parameters (your model path or api key, etc.) in `flashrag/config/basic_config.yaml`; refer to the original FlashRAG repository to download the BM25 index and put it into `indexes`. Put your data under `datasets`. 

2. Configure the running parameters in `run.py`: set you data storage path in the parameter `data_dir`; set the model you want to use in the parameter `GENERATOR_MODELS`; set the dataset you want to run in the parameter `DATASET_NAMES`; select the method you want to run in parameter `FUNC_DICT`; set other parameters under the main method (such as the log storage path). 

3. Run `run.py` and observe the experimental results after completed. 