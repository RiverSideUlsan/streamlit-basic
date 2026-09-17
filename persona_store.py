from pathlib import Path


PERSONA_DIRECTORY = Path(__file__).parent / "personas"


def load_persona(persona):
    """Markdown에 작성한 캐릭터 설정을 채팅용 정보로 읽는다."""
    markdown = (PERSONA_DIRECTORY / persona["file_name"]).read_text(encoding="utf-8")
    intro = markdown.split("## 한 줄 소개", maxsplit=1)[1].split("##", maxsplit=1)[0].strip()

    return {
        **persona,
        "intro": intro,
        "system": f"다음 캐릭터 페르소나를 일관되게 반영해 대화하세요.\n\n{markdown}",
    }
