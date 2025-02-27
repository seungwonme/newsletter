from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults

from src.agent.utils.file_utils import save_text_to_unique_file

load_dotenv()


def main():
    search = DuckDuckGoSearchResults(output_format="list")

    query = "거시경제 site:bbc.com"
    result = search.invoke(query)

    content = "# DuckDuckGo Search\n\n"
    for i in range(len(result)):
        r = result[i]
        content += "## " + r["title"] + "\n" + r["link"] + "\n" + r["snippet"] + "\n\n"

    save_text_to_unique_file(content, file_name="duckduckgo_search.md")


if __name__ == "__main__":
    main()

# https://duckduckgo.com/duckduckgo-help-pages/results/syntax/
# https://python.langchain.com/docs/integrations/tools/ddg/
# https://python.langchain.com/api_reference/community/tools/langchain_community.tools.ddg_search.tool.DuckDuckGoSearchResults.html#langchain_community.tools.ddg_search.tool.DuckDuckGoSearchResults.backend
