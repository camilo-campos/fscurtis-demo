import os
from langchain.prompts import PromptTemplate
from langchain_ibm import WatsonxLLM
from langchain_core.output_parsers import StrOutputParser



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


def nueva_cotizacion(cliente:str , fecha_actual:str , validez:str , productos:str , terminos:str):

    generate_prompt = PromptTemplate(
        template="""

        <|begin_of_text|>

        <|start_header_id|>system<|end_header_id|>
        You are an artificial intelligence assistant whose task is to create a quote for a customer for our products in table format as shown below , you are expected in your response to return the tables but with the customer information , dates , products , terms and conditions .
        Also your answers should always be in English and in table format.
        
        Formato Sugerido para una Cotización.
        A continuación se presenta un formato básico que puedes utilizar como guía para crear tu propia cotización:
        Nombre de la Empresa	 | FSCurtis
        Nombre del Cliente	     |[Cliente]
        Fecha	                 |[Fecha Actual]
        Validez de Cotización	 |[Fecha de Validez]
        
        Detalle de Productos/Servicios
        Código	   | Descripción	                  |  Cantidad	      |  Precio Unitario  |	     Subtotal
        [Código 1] |	[Descripción del Producto 1]  |	[Cantidad 1]	  |   [Precio 1]	  |       [Subtotal 1]
        [Código 2] |	[Descripción del Producto 2]  |	[Cantidad 2]	  |   [Precio 2]	  |       [Subtotal 2]
                                                                                              |   Total:
                                                                                              |  [Total General]
        Términos y Condiciones:
         Método de pago: [Especificar]
         Políticas de devolución: [Especificar]
         Otros: [Especificar]
        <|eot_id|>

        <|start_header_id|>user<|end_header_id|>

        nombre del cliente :{cliente}
        fecha actual : {fecha_actual}
        validez de cotizacion : {validez}
        productos deseados : {productos}
        terminos y condicones : {terminos}
        Answer:

        <|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>""",
        input_variables=["cliente","fecha_actual","validez","productos","terminos"],
    )

    # Chain
    analizar = generate_prompt | llama_3_model | StrOutputParser()


    resultado=analizar.invoke({"cliente":cliente,"fecha_actual":fecha_actual,"validez":validez,"productos":productos ,"terminos":terminos})
    #print(resultado)
    return resultado