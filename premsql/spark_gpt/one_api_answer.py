# !/usr/bin/python3
# -*- coding: utf-8 -*-
import os

from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_fixed

from premsql.spark_gpt.dotmap_cus import DotMap
from setting import BASE_DIR

from premsql.constants.llm_cons import TONGYI_API_KEY, TONGYI_MODEL_NAME


class AnswerByOneAPI:
    def __init__(self, c):
        self.c = DotMap(c)
        self.s = DotMap()

    @retry(stop=stop_after_attempt(6), wait=wait_fixed(2))
    def call_one_api(self):
        client = OpenAI(
            # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
            api_key=TONGYI_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        prompt_str=self.c.question
        completion = client.chat.completions.create(
            model=TONGYI_MODEL_NAME,  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'user', 'content': prompt_str}],
        )
        resp_json = completion.model_dump_json()
        print(resp_json)
        self.s.answer = completion.choices[0].message.content
        logger.debug(f'llm_answer: {self.s.answer}')

    def answer_one_api(self):
        self.call_one_api()
        pass

    def main(self):
        self.answer_one_api()
        pass


if __name__ == '__main__':
    qq = {
        "question": """
        今天天气如何
        """,
        "chat_history":""

    }
    AnswerByOneAPI(qq).main()
    pass
