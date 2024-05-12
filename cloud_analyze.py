from google.cloud import language_v1

client = language_v1.LanguageServiceClient()

# Analyze text
document = language_v1.Document(content=user_query, type_=language_v1.Document.Type.PLAIN_TEXT)
response = client.analyze_sentiment(request={'document': document})
sentiment = response.document_sentiment.score
