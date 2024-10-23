import base64
import io
from typing import Optional

import pandas as pd
from premsql.generators.base import Text2SQLGeneratorBase
from premsql.pipelines.base import ChartPlotWorkerBase, ChartPlotWorkerOutput
from premsql.pipelines.baseline.prompts import BASELINE_CHART_WORKER_PROMPT_TEMPLATE
from premsql.pipelines.tools.plot.base import BasePlotTool
from premsql.pipelines.utils import convert_df_to_dict

class BaseLinePlotWorker(ChartPlotWorkerBase):
    def __init__(self, generator: Text2SQLGeneratorBase, plot_tool: BasePlotTool) -> None:
        self.generator, self.plot_tool = generator, plot_tool
    
    def run(
        self,
        question: str,
        input_dataframe: pd.DataFrame,
        temperature: Optional[float] = 0.1,
        max_new_tokens: Optional[int] = 100,
        prompt_template: Optional[str] = BASELINE_CHART_WORKER_PROMPT_TEMPLATE,
        **kwargs,
    ) -> ChartPlotWorkerOutput:
        prompt = prompt_template.format(
            columns=list(input_dataframe.columns), question=question
        )
        try:
            to_plot = self.generator.generate(
                data_blob={"prompt": prompt},
                temperature=temperature,
                max_new_tokens=max_new_tokens,
                postprocess=False
            )
            to_plot = to_plot.replace("null", "None")
            plot_config = eval(to_plot)
            fig = self.plot_tool.run(data=input_dataframe, plot_config=plot_config)
            output = self.plot_tool.convert_image_to_base64(
                self.plot_tool.convert_plot_to_image(fig=fig)
            )
            return ChartPlotWorkerOutput(
                question=question,
                input_dataframe=convert_df_to_dict(input_dataframe),
                plot_config=plot_config,
                plot_reasoning=None,
                output_dataframe=None,
                image_plot=output,
                error_from_model=None,
                additional_input={
                    "temperature": temperature,
                    "max_new_tokens": max_new_tokens,
                    **kwargs
                }
            )

        except Exception as e:
            error_message = f"Error during plot generation: {str(e)}"
            return ChartPlotWorkerOutput(
                question=question,
                input_dataframe=convert_df_to_dict(input_dataframe),
                plot_config=None,
                image_plot=None,
                plot_reasoning=None,
                error_from_model=error_message,
                additional_input={
                    "temperature": temperature,
                    "max_new_tokens": max_new_tokens,
                    **kwargs,
                },
            )
        
