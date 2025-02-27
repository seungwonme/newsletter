import base64
import os
import os.path
import re
from email.message import EmailMessage
from typing import Optional

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from markdown2 import Markdown
from premailer import transform


def convert_markdown_to_html(markdown_content: str, title: Optional[str] = None) -> str:
    """마크다운 컨텐츠를 이메일용 HTML로 변환합니다.

    Args:
        markdown_content (str): 변환할 마크다운 컨텐츠
        title (Optional[str], optional): HTML 문서의 제목. Defaults to None.

    Returns:
        str: 이메일 클라이언트에 최적화된 HTML 문서
    """
    # markdown2 인스턴스 생성
    markdowner = Markdown(
        extras=[
            "tables",
            "fenced-code-blocks",
            "footnotes",
            "header-ids",
            "images",
        ]
    )

    # 마크다운을 HTML로 변환
    html_content = markdowner.convert(markdown_content)

    # 이메일에 최적화된 스타일이 포함된 HTML 템플릿
    email_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style type="text/css">
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{ font-size: 24px; margin-top: 40px; margin-bottom: 20px; }}
        h2 {{ font-size: 20px; margin-top: 30px; margin-bottom: 15px; }}
        p {{ margin-bottom: 15px; }}
        a {{ color: #0366d6; text-decoration: none; }}
        img {{ max-width: 100%; height: auto; display: block; margin: 15px 0; }}
        .summary {{ background-color: #f8f8f8; padding: 15px; border-left: 4px solid #0366d6; }}
    </style>
</head>
<body>
    {content}
</body>
</html>
    """

    # 스타일이 적용된 전체 HTML 문서 생성
    full_html = email_template.format(title=title or "Newsletter", content=html_content)

    # CSS를 인라인 스타일로 변환 (이메일 클라이언트 호환성)
    inlined_html = transform(full_html)

    # id 속성 제거 (일부 이메일 클라이언트에서 문제 발생 가능)
    inlined_html = re.sub(r' id="[^"]+"', "", inlined_html)

    return inlined_html


# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.addons.current.action.compose",
]


if __name__ == "__main__":
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    # Read the markdown content from the file
    with open("output/newsletter.md", "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Convert markdown to HTML
    content = convert_markdown_to_html(markdown_content)

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        message = EmailMessage()

        # Add the HTML content
        message.add_alternative(content, subtype="html")

        message["To"] = "kstobit@naver.com"
        message["From"] = "news4letter2@gmail.com"
        message["Subject"] = "오늘의 뉴스레터"

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        print(f'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
