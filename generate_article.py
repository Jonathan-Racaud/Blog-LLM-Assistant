import os
import sys
import base64
from getpass import getpass
from langchain_mistralai import ChatMistralAI as Chat
from langchain.prompts import (
        SystemMessagePromptTemplate,
        HumanMessagePromptTemplate
)
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate
from skimage import io
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

api_key = "MISTRAL_API_KEY"
ai_model = "mistral-small-latest"

os.environ[api_key] = os.getenv(api_key)

# For normal accurate responses
llm = Chat(temperature=0.0, model=ai_model)

# For unique creative response
creative_llm = Chat(temperature=0.9, model=ai_model)

# Generate from an article multiple items
# 1. Article title
# 2. Article description
# 3. Graphics (banner, hero, etc)
# 4. Suggestion on how to improve the article

article = """
I think I may have gone mad. I started working on my own programming language.

How it started
I stubbled upon the Crafting Interpreters book and found it very interesting to read. As I never really studied compilers and how they worked, the approach of this book, which is writting a full fledge interpreter for a simple programming language, was very interesting to me.

I am more of a hands on kind of guy when it comes to learning, so that approach was perfect for me. It also does it twice, once in Java and then in C where the author builds a bytecode vm for his language. This is nice to see different ways to accomplish the same task.

Thus I started following the book and implementing the first Java interpreter in the Beef programming language.

I might one day write article on this language as it is a really nice one. Think of C# but with manual memory management.
I didn’t finish the java interpreter though as I find it difficult to follow with the language that I chose to use. The memory management model and Visitor pattern is quite difficult to implement (as used in the book) in Beef as that language has manual memory management. Beef being closer to C than Java, I am now following the C interpreter.

I am primarily using this book to get a grasp on what one would need to do to write its own programming language and this is going well in my opinion, but I’m not here to do a book review. Just go read it if that topic is interesting to you.

You might ask yourself one question:

But why?
 

I have different ideas that I want to test and an urge to put them to the test.

The motivation behind
It is usually said that mathematics is the universal language because everyone that learns it can understand it. You might not learn it in the same way if you are in France or China or the US, but everyone will understand
2
+
2
2+2
or
f
(
x
,
y
)
=
3
x
∗
2
y
π
f(x,y)=3x∗ 
π
2y
​
 

Since programming has its root in maths we could argue that it would be similar, and to some extent, it is but recently I read or heard somewhere that it can be difficult for some people to learn programming not because it is a difficult topic to learn, but rather than the language used in programming is primarily English.

Indeed, the vast majority of knowledge around programming is in English. Let it be youtube videos, conferences, books or blog articles such as this one. As a non native English speaker I can relate to that sentiment and so I started wondering:

What would a programming language look like without keywords?
Is it possible to design a language where the different constructs could be abstracted away from any keyword?
Can such a language be relatively easy to learn?
Also, can it not become an unreadable soupe of characters on your screen?
In the same way that we learn about the different mathematics concepts with our own natural words which can differ from languages to languages. I want to see if we can do the same with programming languages.

I want to explore if it is possible to learn and use what is a while loop, an if condition or a return without having those concept tied to those keywords.

This is the primary force driving me in this endeavour.

Alas a programming language is not only its syntax. It is also the semantic behind and the different concepts and paradigm that one can use. I do have the ambition of taking the features that I like from the other languages that I use on a day to day basis or not, but I also try to not look too much in how they present it as well so that (I hope) I can be as free of their influence as I can.

I’m sure that I’ll reinvent a lot of wheels along the way, but that’s okay because the primary goal is acquiring knowledge for myself. This must sounds weird to others, not wanting to read too much how other people did it, but that’s how I want to work at the moment.

I do intend to have a working product, it is part of my set goals, but I would consider it a bonus if even one person apart from me uses it.

Another goal for me is to share what I learn along the way with you.

The next steps
This article was only the introduction of what I hope will be a long and interesting serie of articles.

I already have most of the syntax and features that I want scattered around my notes, so the next parts will go more in the details of the language:

What does it looks like.
What features I’d like it to have.
Hope to see you in the next one!
"""

if len(sys.argv) > 1:
    article = sys.argv[1]

# Preparing our prompts

# Defines the system prompt (how the AI should act)
system_title_prompt = SystemMessagePromptTemplate.from_template(
        "You are an AI assistant that helps generate article titles."
)

# The user prompt is provided by the user, in this case however the only dynamic part is the article
user_title_prompt = HumanMessagePromptTemplate.from_template(
        """You are tasked with crating a name for a article.
        The article is here for you to examine:

        ---

        {article}
        
        ---

        The name should be based of the context of the article.
        Be creative, but make sure the names are clear, catchy, and relevant to the theme of the article.

        Only output the article name, no other explanation or text can be provided.""",
        input_variables=["article"]
)

title_prompt = ChatPromptTemplate.from_messages([system_title_prompt, user_title_prompt])

chain_one = (
    {
        "article": lambda x: x["article"],
    }
    | title_prompt
    | creative_llm
    | {"article_title": lambda x: x.content}
)

print("Asking to generate article's title")

article_title_response = chain_one.invoke({"article": article})
article_title = article_title_response['article_title']

system_seo_prompt = SystemMessagePromptTemplate.from_template(
        "You are an AI assistant that helps build good articles."
)

user_seo_prompt = HumanMessagePromptTemplate.from_template(
        """You are tasked with creating a description for the article. The article is here for you to examine:

        ---

        {article}

        ---

        Here is the article title '{article_title}'.

        Output the SEO friendly article description. Do not output anything other than the description.""",
        input_variables=["article", "article_title"]
)

seo_prompt = ChatPromptTemplate.from_messages([system_seo_prompt, user_seo_prompt])

chain_two = (
    {
        "article": lambda x: x["article"],
        "article_title": lambda x: x["article_title"]
    }
    | seo_prompt
    | llm
    | {"article_description": lambda x: x.content}
)

print("Asking to generate article's description")

article_description_response = chain_two.invoke({"article": article, "article_title": article_title})
article_description = article_description_response['article_description']

user_editor_prompt = HumanMessagePromptTemplate.from_template(
        """You are tasked with reading and analyzing the following article:

        ---

        {article}

        ---

        Provide constructive feedback to the user so they can learn where to improve their own writing.""",
        input_variables=["article"]
)

editor_prompt = ChatPromptTemplate.from_messages([
    system_seo_prompt,
    user_editor_prompt
])


class Paragraph(BaseModel):
    feedback: str = Field(description="Constructive feedback on the original paragraph")

structured_llm = creative_llm.with_structured_output(Paragraph)

chain_three = (
        {
            "article": lambda x: x["article"]
        }
        | editor_prompt
        | structured_llm
        | {
            "feedback": lambda x: x.feedback
          }
)

print("Asking to provide feedback on the article")

editor_response = chain_three.invoke({"article": article})

image_prompt = PromptTemplate(
        input_variables=["article"],
        template=(
            "Generate a prompt with less than 500 characters to generate an image"
            "based on the following article: {article}"
        )
)

def generate_image(image_prompt):
    print("Asking to generate an image")

    image_llm = ChatGoogleGenerativeAI(model="models/gemini-2.0-flash-preview-image-generation")
    image_response = image_llm.invoke(
            [image_prompt],
            generation_config=dict(response_modalities=["TEXT", "IMAGE"])
    )
    image_block = next(
            block
            for block in image_response.content
            if isinstance(block, dict) and block.get("image_url")
    )
    
    image_data = image_block["image_url"].get("url").split(",")[-1]

    with open("output/image.png", "wb") as image_file:
        image_file.write(base64.b64decode(image_data))

image_gen_runnable = RunnableLambda(generate_image)

chain_four = (
        {
            "article": lambda x: x['article']
        }
        | image_prompt
        | creative_llm
        | (lambda x: x.content)
        | image_gen_runnable
)

chain_four.invoke({"article": article})

with open("output/title.txt", "w") as title_file:
    title_file.write(article_title)

with open("output/description.txt", "w") as description_file:
    description_file.write(article_description)

with open("output/feedback.txt", "w") as improvement_file:
    improvement_file.write(editor_response['feedback'])

print("Writer assistant work finished")
print("==============================")
