from services.groq_client import GroqClient

client = GroqClient()

response = client.generate("Explain Risk in contractor in term in simple terms")

print("\n✅ Response:\n")
print(response)