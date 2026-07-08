import asyncio

from team import (
    senior_idea_analyst,
    senior_strategist,
    senior_react_engineer,
    senior_content_editor,
)

from autogen_agentchat.conditions import (
    MaxMessageTermination,
)
from autogen_agentchat.messages import BaseChatMessage, TextMessage

INPUTS = {

}


async def main():
    try:
        # Step-by-step sequential execution.
        #
        # `history` accumulates every step's real conversation so far and is
        # threaded into each subsequent step's .run() call. Without this,
        # each step only ever sees its own task prompt in isolation - later
        # steps (e.g. "review the draft") have no way to see what an earlier
        # step (e.g. "draft the posting") actually produced.
        history: list[BaseChatMessage] = []
        # ==================================================
        # Workflow Step: task_expand_idea
        # Workflow Edge: task_expand_idea -> task_refine_idea
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_expand_idea")
        print("=" * 80)

        task_prompt = """THIS IS A GREAT IDEA! Analyze and expand it by conducting a comprehensive research.

Final answer MUST be a comprehensive idea report detailing why this is a great idea, the value proposition, unique selling points, why people should care about it and distinguishing features.

IDEA:
# ----------
{idea} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_idea_analyst, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_idea_analyst.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_refine_idea
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_refine_idea")
        print("=" * 80)

        task_prompt = """Expand idea report with a Why, How, and What messaging strategy using the Golden Circle Communication technique, based on the idea report.

Your final answer MUST be the updated complete comprehensive idea report with WHY, HOW, WHAT, a core message, key features and supporting arguments.

YOU MUST RETURN THE COMPLETE IDEA REPORT AND THE DETAILS, You'll get a $100 tip if you do your best work! """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_strategist, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_strategist.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_choose_template
        # Workflow Edge: task_choose_template -> task_update_page
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_choose_template")
        print("=" * 80)

        task_prompt = """Learn the templates options choose and copy the one that suits the idea below the best, YOU MUST COPY, and then YOU MUST read the src/component in the directory you just copied, to decide what component files should be updated to make the landing page about the idea below.

- YOU MUST READ THE DIRECTORY BEFORE CHOOSING THE FILES.
- YOU MUST NOT UPDATE any Pricing components.
- YOU MUST UPDATE ONLY the 4 most important components.

Your final answer MUST be ONLY a JSON array of components full file paths that need to be updated.

IDEA
# ----------
{idea} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_react_engineer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_react_engineer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_update_page
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_update_page")
        print("=" * 80)

        task_prompt = """READ the ./[chosen_template]/src/app/page.jsx OR ./[chosen_template]/src/app/(main)/page.jsx to learn its content and then write an updated version to the filesystem that removes any section related components that are not in our list from the returns. Keep the imports.

Final answer MUST BE ONLY a valid json list with the full path of each of the components we will be using, the same way you got them.

RULES
# -----
- NEVER ADD A FINAL DOT to the file content.
- NEVER WRITE \n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Save the file as with `.jsx` extension.
- Return the same valid JSON list of the components your got.

You'll get a $100 tip if you follow all the rules!

Also update any necessary text to reflect this landing page is about the idea below.

IDEA
# ----------
{idea} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_react_engineer, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_react_engineer.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_component_content
        # Workflow Edge: task_component_content -> task_update_component
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_component_content")
        print("=" * 80)

        task_prompt = """A engineer will update the {component} (code below), return a list of good options of texts to replace EACH INDIVIDUAL existing text on the component, the suggestion MUST be based on the idea below, and also MUST be similar in length with the original text, we need to replace ALL TEXT.

NEVER USE Apostrophes for contraction! You'll get a $100 tip if you do your best work!

IDEA
# -----
{expanded_idea}

REACT COMPONENT CONTENT
# -----
{file_content} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_content_editor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_content_editor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_update_component
        # Workflow Edge: task_update_component -> task_qa_component
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_update_component")
        print("=" * 80)

        task_prompt = """YOU MUST USE the tool to write an updated version of the react component to the file system in the following path: {component} replacing the text content with the suggestions provided.

You only modify the text content, you don't add or remove any components.

RULES
# -----
- Remove all the links, this should be single page landing page.
- Don't make up images, videos, gifs, icons, logos, etc.
- keep the same style and tailwind classes.
- MUST HAVE 'use client' at the be beginning of the code.
- href in buttons, links, NavLinks, and navigations should be `#`.
- NEVER WRITE \n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- Keep the same component imports and don't use new components.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Save the file as with `.jsx` extension.

If you follow the rules I'll give you a $100 tip!!! MY LIFE DEPEND ON YOU FOLLOWING IT!

CONTENT TO BE UPDATED
# -----
{file_content} """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_content_editor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_content_editor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        # ==================================================
        # Workflow Step: task_qa_component
        # ==================================================
        print("\n" + "=" * 80)
        print("Executing step: task_qa_component")
        print("=" * 80)

        task_prompt = """Check the React component code to make sure it's valid and abide by the rules below, if it doesn't then write the correct version to the file system using the write file tool into the following path: {component}.

Your final answer should be a confirmation that the component is valid and abides by the rules and if you had to write an updated version to the file system.

RULES
# -----
- NEVER USE Apostrophes for contraction!
- ALL COMPONENTS USED SHOULD BE IMPORTED.
- MUST HAVE 'use client' at the be beginning of the code.
- href in buttons, links, NavLinks, and navigations should be `#`.
- NEVER WRITE \n (newlines as string) on the file, just the code.
- NEVER FORGET TO CLOSE THE FINAL BRACKET (}}) in the file.
- NEVER USE COMPONENTS THAT ARE NOT IMPORTED.
- ALL COMPONENTS USED SHOULD BE IMPORTED, don't make up components.
- Always use `export function` for the component class.

You'll get a $100 tip if you follow all the rules! """
        history.append(TextMessage(content=task_prompt, source="user"))
        # Execute via the assigned agent: senior_content_editor, passing the
        # accumulated history so this step can see every prior step's output.
        result = await senior_content_editor.run(task=history)
        history = [m for m in result.messages if isinstance(m, BaseChatMessage)]

        # Print step output
        if hasattr(result, "messages") and result.messages:
            print(result.messages[-1].content)
        else:
            print(result)

        print("\n" + "=" * 80)
        print("DONE")
        print("=" * 80)

    except Exception as e:
        print("\n" + "=" * 80)
        print("ERROR")
        print("=" * 80)
        print(type(e).__name__)
        print(str(e))



if __name__ == "__main__":
    asyncio.run(main())