# LangChain Dependencies
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langgraph.graph import END, StateGraph
# For State Graph
from typing_extensions import TypedDict
import os
from langchain_groq import ChatGroq
from typing import Annotated
from langchain_ibm import WatsonxLLM
from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import MemorySaver



llama_3_model = WatsonxLLM(
    model_id="meta-llama/llama-3-70b-instruct",
    url="https://us-south.ml.cloud.ibm.com",
    apikey="0GY8cqsa49R8Gs6aiK0RB5Hb6ZRDFyKew474yYfVJBKa",
    project_id="37e2e673-598a-4dca-af77-b102ee3b47c9",
    params={
  "decoding_method": "greedy",
  "max_new_tokens": 4096,
  "min_new_tokens": 0,
  "stop_sequences": [
   ";"
  ],
  "repetition_penalty": 1
 },
    )



paciente_prompt = PromptTemplate(
    template="""

    <|begin_of_text|>

    <|start_header_id|>system<|end_header_id|>
    You are an artificial intelligence assistant named Carlos whose task is to help users with their queries about the products available in the fs curtis store you work for, in your answers you must answer only questions related to the store and the products we sell, do not repeat hello all the time in your answers and also your answers must always be in Spanish..
    your product answers should be based on the following products only.
    products available:
    Compresor CA - 5 HP - 15 HP.
        For heavy industry, CA series components are selected based on durability and performance. If you are looking for performance in demanding or “heavy-duty” applications, CA series compressors are the best choice.
    
    Compresor centrífugos - Serie EcoTurbo - Refrigerados por aire o agua.
        Lower maintenance costs and extended service life. Oil-free centrifugal compressors combine decades of FS-Elliott experience with FS-Curtis' reputation as a supplier of lubricated compressors. The ECO-Turbo series of compressors is ideal for a wide range of applications where 100% oil-free compressed air is required at high flow rates ranging from 185 kW to 250 kW and pressures in the order of 125 PSI. The compressor's simple and interlocked design offers high reliability and guarantees safe operation, even in extreme conditions. FS-Elliott's titanium impellers ensure optimum efficiency and long service life. The Eco-Turbo series is easy to install, operate and maintain, making them the optimal choice when compressed air quality is paramount. (*) Compared to oil-free screw compressors.
    
    Compresor CT - 5 HP - 10 HP.
        The CT and CTS series piston compressors combine FS-Curtis' signature performance and reliability with a simple industrial design, making them the most rugged and affordable compressors in their class.
    <|eot_id|>

    <|start_header_id|>user<|end_header_id|>

    Text: {text}
    Answer:

    <|eot_id|>

    <|start_header_id|>assistant<|end_header_id|>""",
    input_variables=["text"],
)

# Chain
asistente_chain = paciente_prompt | llama_3_model | StrOutputParser()




class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    


graph_builder = StateGraph(State)

def chatbot(state: State):

    question = state["messages"]
    
    return {"messages": [asistente_chain.invoke({"text":question })]}



# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)

graph_builder.set_entry_point("chatbot")

graph_builder.set_finish_point("chatbot")



memory2 = MemorySaver()

graph = graph_builder.compile(checkpointer=memory2)


# Asegúrate de que 'graph' está definido y configurado correctamente
def process_user_message(user_input: str , id_sesion:str ) -> str:
    config = {"configurable": {"thread_id": id_sesion}}
    try:
        # Ejecuta la invocación
        events = graph.invoke({"messages": [("user", user_input )]}, config, stream_mode="values")
        
        # Verifica el formato de 'events' y extrae el contenido
        if not events or not isinstance(events, dict) or "messages" not in events:
            raise ValueError("No se recibieron mensajes del chatbot o formato incorrecto.")
        
        # Imprime 'events' para depuración
        print(events)
        
        # Extrae el contenido del último mensaje
        # Asegúrate de que 'events["messages"]' contenga objetos de tipo 'HumanMessage'
        last_message = events["messages"][-1]
        result = last_message.content if hasattr(last_message, 'content') else "No content found"
        print(result)
        return result

    except Exception as e:
        raise RuntimeError(f"Error procesando el mensaje del usuario: {str(e)}")