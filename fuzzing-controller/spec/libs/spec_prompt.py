DEPENDENCY_KEYWORD = "Statement does hold"
CMD_DEPENDENCY_PROMPT = """
You are a Zigbee expert.

Followings are descriptions of a Zigbee cluster command called "{}".
"{}"

Followings are descriptions of another Zigbee cluster command called "{}".
"{}"

Please base on the above command description and determine if the following statement holds: "The consequence of the first command execution explicitly updates some device properties which the second command explicitly checks/examines before execution".
Think step by step and show your thought.
Finally, summarize your answer in one sentence: """ + f""" "{DEPENDENCY_KEYWORD}" or "Statement does not hold"."""


DESCRIPTION_SUMMARY_PROMPT = """
You are a Zigbee expert.

Followings are descriptions of a Zigbee cluster command called "{}".
{}

You are requried to summarize the description to the command within 500 words. In particular, summarize the comamnd's purpose, functionality, and influence on the Zigbee device once the command is successfully executed.
"""