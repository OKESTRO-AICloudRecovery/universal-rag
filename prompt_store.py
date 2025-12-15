analysis_prompt = """Please analyze shape, characteristic and relationship of the following all time-series performance metric that collected in failure incident related VM comprehensively. he performance metrics have been abstracted into our own LLM-friendly syntax. To help with basic understanding, examples will be provided to show what this syntax means in time-series format. When analyzing the following performance metrics, you'll need to develop your understanding further on your own, building upon this basic understanding to identify features that are unique to each performance metric.
Include numerical insights of statistics and metadata also in your analysis. At this time, judgments about whether a number is high or low follow the objective level of statistical data. the analysis must processed focusing on the abnormal parts, assuming that the metrics are normal. If there are no abnormal points, please conclude it is normal.
The answer must detail with in-depth insights, and include only the core conclusion. Also, it have to be written by only based on fact, eliminating opinions. Please verify these things yourself before answering.
"""
agentic_prompt = """You are a site reliability engineer. An incident ticket of unknown causes has been declared on a cloud system for which you are responsible and you are tasked with resolving it.
The analytical report below presents observational insights for each performance metric collected from the VM involved in the incident.
Based on the analytical report, please identify what failure most likely to be the root cause of the incident is and suggest how should we response it.
When considering the basis for a diagnosis, if there is a historical predicted failure marked as incorrect in the metric on which it is based, the failure can not be regarded a root cause failure. And the identification of the root cause failure should done as a presenting its name in final.

=====================
Analytical report of performance metric:
{}
=====================
Diagnostics result(root cause failure):"""
