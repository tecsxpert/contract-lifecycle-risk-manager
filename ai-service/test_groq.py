from groq_client import GroqClient

if __name__ == "__main__":
    print("Starting Groq API test call...")
    client = GroqClient()
    try:
        models = client.fetch_models()
        print("Groq API call succeeded. Response:")
        print(models)
    except Exception as error:
        print("Groq API call failed:", error)
        raise
