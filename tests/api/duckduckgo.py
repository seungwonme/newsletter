from pprint import pprint

from a.agent.utils.file_utils import save_text_to_unique_file
from dotenv import load_dotenv
from langchain_community.tools import DuckDuckGoSearchResults

load_dotenv()


def main():
    search = DuckDuckGoSearchResults(output_format="list", num_results=10)

    query = "거시경제 site:www.bbc.com"
    result = search.invoke(query)
    pprint(result)

    content = "# DuckDuckGo Search\n\n"
    for i in range(len(result)):
        r = result[i]
        content += "## " + r["title"] + "\n" + r["link"] + "\n" + r["snippet"] + "\n\n"

    save_text_to_unique_file(content, file_name="duckduckgo_search.md")


if __name__ == "__main__":
    main()

# https://duckduckgo.com/duckduckgo-help-pages/results/syntax/
# https://python.langchain.com/docs/integrations/tools/ddg/
# https://python.langchain.com/api_reference/community/tools/langchain_community.tools.ddg_search.tool.DuckDuckGoSearchResults.html
