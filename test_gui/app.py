import gradio as gr
from gov_chat.webscrape import generatre_site_map,scan_sitemap
from gov_chat.splitandstore import split_and_load_docs
from gov_chat.query_vs import interregate_vs
from gov_chat.util import purge_directory
from gov_chat.query_bot import ChatBot
from langchain.vectorstores import Chroma
def update_chatbot_collection(evt: gr.SelectData,chatbot:ChatBot):
    chatbot.select_colleciton(evt.value)

with gr.Blocks() as demo:
    with gr.Tab("1. Sitemap Generation"):
        website = gr.Text(label="Target Website")
        safe_count = gr.Number(label="Max number of routes to grab",value=200)
        save_directory = gr.Text(label="Save Directory", value="./outputs")
        save_file = gr.Text(label="Sitemap filename", value = "sitemap.json")
        sitemap_button = gr.Button("Generate Sitemap") 
        links_scanned = gr.Number(label="Links Scanned")
        links = gr.JSON(label="Discovered URLs")
        sitemap_button.click(generatre_site_map,inputs=[
            website,safe_count,save_directory,save_file
        ],outputs=[links,links_scanned]
        )
    with gr.Tab("2. Site Scanner"):
        purge_docs = gr.Button("Purge Docs")
        site_map_file = gr.Text("./outputs/sitemap.json")
        batch_count = gr.Number(value=10,label="Batch Count")
        output_directory = gr.Text(value="./outputs/docs",label="Output directory")
        scan_site_button = gr.Button("Scan Site")

        lookup = gr.JSON(label="Scanned URLs to Docs")
        scan_site_button.click(
            scan_sitemap,inputs=[
                site_map_file,batch_count,output_directory
            ],
            outputs= [lookup]
        )
        purge_docs.click(
            purge_directory,
            inputs=[output_directory]

        )

    with gr.Tab("3. Split and Store"):
        document_directory = gr.Text(value = "./outputs/docs",label="Document directory")
        chunk_size = gr.Number(value = 500, label="Chunk size")
        chunk_overlap = gr.Number(value = 0, label="Chunk overlap")
        colleciton_name = gr.Text(value = Chroma._LANGCHAIN_DEFAULT_COLLECTION_NAME,label="Colleciton")
        split_and_store_button = gr.Button("Split and Store Documents")
        split_and_store_button.click(
            split_and_load_docs,inputs=[
                document_directory,chunk_size,chunk_overlap,colleciton_name
            ]
        )
    with gr.Tab("4. Query Vector Store"):
        gr.ChatInterface(interregate_vs)
    
    with gr.Tab("4. Query Bot(GPU Required)") as test:
        chatbot = ChatBot()
        colleciton_list = gr.Dropdown(chatbot.get_collections(),value=chatbot.get_collections()[0],label="Collection queried")
        colleciton_list.select(chatbot.select_collection,inputs=[colleciton_list])

        gr.ChatInterface(chatbot.ask_bot)



if __name__ =="__main__":
    demo.launch()