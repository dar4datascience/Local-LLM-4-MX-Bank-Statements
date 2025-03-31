library(ellmer)

chat <- chat_ollama(model = "llava:7b")
chat$chat("Tell me three jokes about statisticians")

chat$chat(
  content_image_file("example_image.jpg"),
  "What animal is in this image? Describe it, please."
)
















