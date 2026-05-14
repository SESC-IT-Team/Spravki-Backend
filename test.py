import asyncio

from document_renderer_sdk.client import AsyncDocumentRendererClient

async def main():
    async with AsyncDocumentRendererClient() as client:
        task_id = await client.render_document(
            template_content=...,
            data=...,
            filename="output67.pdf"
        )


if __name__ == '__main__':
    asyncio.run(main())