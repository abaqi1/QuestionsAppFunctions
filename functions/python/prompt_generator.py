
from openai import OpenAI
import os


api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
client = OpenAI(api_key=api_key)

META_PROMPT = """
Given a task description or existing prompt, produce a detailed system prompt to guide a language model in completing the task effectively.

# Guidelines

- Understand the Task: Grasp the main objective, goals, requirements, constraints, and expected output.
- Minimal Changes: If an existing prompt is provided, improve it only if it's simple. For complex prompts, enhance clarity and add missing elements without altering the original structure.
- Reasoning Before Conclusions**: Encourage reasoning steps before any conclusions are reached. ATTENTION! If the user provides examples where the reasoning happens afterward, REVERSE the order! NEVER START EXAMPLES WITH CONCLUSIONS!
    - Reasoning Order: Call out reasoning portions of the prompt and conclusion parts (specific fields by name). For each, determine the ORDER in which this is done, and whether it needs to be reversed.
    - Conclusion, classifications, or results should ALWAYS appear last.
- Examples: Include high-quality examples if helpful, using placeholders [in brackets] for complex elements.
   - What kinds of examples may need to be included, how many, and whether they are complex enough to benefit from placeholders.
- Clarity and Conciseness: Use clear, specific language. Avoid unnecessary instructions or bland statements.
- Formatting: Use markdown features for readability. DO NOT USE ``` CODE BLOCKS UNLESS SPECIFICALLY REQUESTED.
- Preserve User Content: If the input task or prompt includes extensive guidelines or examples, preserve them entirely, or as closely as possible. If they are vague, consider breaking down into sub-steps. Keep any details, guidelines, examples, variables, or placeholders provided by the user.
- Constants: DO include constants in the prompt, as they are not susceptible to prompt injection. Such as guides, rubrics, and examples.
- Output Format: Explicitly the most appropriate output format, in detail. This should include length and syntax (e.g. short sentence, paragraph, JSON, etc.)
    - For tasks outputting well-defined or structured data (classification, JSON, etc.) bias toward outputting a JSON.
    - JSON should never be wrapped in code blocks (```) unless explicitly requested.

The final prompt you output should adhere to the following structure below. Do not include any additional commentary, only output the completed system prompt. SPECIFICALLY, do not include any additional messages at the start or end of the prompt. (e.g. no "---")

[Concise instruction describing the task - this should be the first line in the prompt, no section header]

[Additional details as needed.]

[Optional sections with headings or bullet points for detailed steps.]

# Steps [optional]

[optional: a detailed breakdown of the steps necessary to accomplish the task]

# Output Format

[Specifically call out how the output should be formatted, be it response length, structure e.g. JSON, markdown, etc]

# Examples [optional]

[Optional: 1-3 well-defined examples with placeholders if necessary. Clearly mark where examples start and end, and what the input and output are. User placeholders as necessary.]
[If the examples are shorter than what a realistic example is expected to be, make a reference with () explaining how real examples should be longer / shorter / different. AND USE PLACEHOLDERS! ]

# Notes [optional]

[optional: edge cases, details, and an area to call or repeat out specific important considerations]
""".strip()

TASK = """
I want to design an AI agent that generates questions for a group chat. 
The Core App Feature is a group, which is a group chat. Every group has metadata containing shared interests of group members and the dynamic of the group. 
Interests and dynamics are set at group creation and can be edited after the creation.
The interests of the group are very important. An AI agent will be sending a question according to the groups interests in the chat every day. The better the questions, the more users will answer, which will create moments of good user experience. 
The dynamic is also important for the agent. It could be a group of young men, a family group, a group fascinated by a particular sports team or field of study, or 2 signifiant others. The tone of the question should be appropriate for the dynamic.
Interests can range from generic things like sports, fashion, music, travel, hobbies, politics to specific sports, teams, technologies, celebrities, musicians, meme culture, stocks, travel, hobbies, and bonding. There should be generic interests like bonding that should be part of every group.
The questions that the agent comes up with are crucial to the success of this app. Good questions are the ones that will engage each user to write responses and read others responses. 
Help me write the prompt engineering for this Agent to understand a groups dynamic and interests, and craft questions.
"""

def generate_prompt():
  task_or_prompt = TASK
  completion = client.chat.completions.create(
      model="gpt-4o",
      messages=[
          {
              "role": "system",
              "content": META_PROMPT,
          },
          {
              "role": "user",
              "content": "Task, Goal, or Current Prompt:\n" + task_or_prompt,
          },
      ],
  )

  return completion.choices[0].message.content