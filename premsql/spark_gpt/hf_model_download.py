#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from datasets import load_dataset
from huggingface_hub import hf_hub_download
from transformers import AutoTokenizer, AutoModel
proxy_url = "http://127.0.0.1:7890"
hugging_face_token=""
hugging_face_mirror="https://hf-mirror.com"
class HuggingFaceDownloader:
    def __init__(self):
        # 1. 设置代理
        self.setup_proxy()
        # 2. 设置token（如果需要）
        self.setup_token()
        
    def setup_proxy(self, http_proxy=proxy_url,
                    https_proxy=proxy_url):
        """设置代理"""
        os.environ['HTTP_PROXY'] = http_proxy
        os.environ['HTTPS_PROXY'] = https_proxy
        print("代理设置完成 | Proxy setup completed")
        
    def setup_token(self, token=hugging_face_token):
        """设置Hugging Face token"""
        if token:
            os.environ['HUGGING_FACE_HUB_TOKEN'] = token
            print("Token设置完成 | Token setup completed")
    
    def download_model(self, model_name, save_path):
        """下载模型"""
        try:
            print(f"开始下载模型 | Start downloading model: {model_name}")
            
            # 下载tokenizer
            tokenizer = AutoTokenizer.from_pretrained(model_name, 
                                                    cache_dir=save_path,
                                                    trust_remote_code=True,
                                                                    # mirror=hugging_face_mirror
                                                                    )

            
            # 下载模型
            model = AutoModel.from_pretrained(model_name,
                                            cache_dir=save_path,
                                            trust_remote_code=True,
                                            # mirror=hugging_face_mirror
                                            )
            
            print(f"模型下载完成 | Model downloaded to: {save_path}")
            return True
            
        except Exception as e:
            print(f"模型下载失败 | Model download failed: {str(e)}")
            return False
    
    def download_dataset(self, dataset_name, save_path, subset=None, split=None):
        """下载数据集"""
        try:
            print(f"开始下载数据集 | Start downloading dataset: {dataset_name}")
            
            # 创建保存目录
            os.makedirs(save_path, exist_ok=True)
            
            # 下载数据集
            if subset:
                dataset = load_dataset(dataset_name, subset, cache_dir=save_path)
            else:
                dataset = load_dataset(dataset_name, cache_dir=save_path)
            
            # 如果指定了特定的split，则只获取该split
            if split:
                dataset = dataset[split]
            
            print(f"数据集下载完成 | Dataset downloaded to: {save_path}")
            print(f"数据集信息 | Dataset info:")
            print(dataset)
            
            return dataset
            
        except Exception as e:
            print(f"数据集下载失败 | Dataset download failed: {str(e)}")
            return None

def main():
    # 创建下载器实例
    downloader = HuggingFaceDownloader()
    
    # 设置保存路径
    MODEL_PATH = "./models"
    DATASET_PATH = "./datasets"
    
    # 创建保存目录
    os.makedirs(MODEL_PATH, exist_ok=True)
    os.makedirs(DATASET_PATH, exist_ok=True)
    
    # 示例：下载模型
    MODEL_NAME = "bert-base-chinese"
    downloader.download_model(MODEL_NAME, MODEL_PATH)
    
    # 示例：下载数据集
    DATASET_NAME = "msra_ner"  # 中文命名实体识别数据集
    dataset = downloader.download_dataset(DATASET_NAME, DATASET_PATH, split="train")

if __name__ == "__main__":
    main()