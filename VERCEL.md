### 🚀 Deploying the Telegram Bot to Vercel

Follow these steps to deploy your Python FastAPI Telegram bot to **Vercel**:

1. **Prepare Your FastAPI App**

   * Ensure your main file (e.g., `main.py`) includes:

     ```css
    project/
    │
    ├── api/
    │   └── webhook.py         ← main FastAPI app
    │
    ├── src/
    │   └── prompt.py
    │
    ├── requirements.txt
    ├── vercel.json
    └── .env.example

     ```
   * Expose your bot’s webhook endpoint inside this app.

2. **Add a `vercel.json` File**
  ```json
    {
      "builds": [
          {
              "src": "api/webhook.py",
              "use": "@vercel/python"
          }
      ],
      "routes": [
          {
              "src": "/webhook",
              "dest": "api/webhook.py"
          },
          {
              "src": "/",
              "dest": "api/webhook.py"
          }
      ]
  }
  ```


3. **Install Dependencies**

   * Your  `requirements.txt` file containing:

     ```
     fastapi
     uvicorn
     python-telegram-bot
     ```
   * Include any other packages your bot uses.

4. **Set Environment Variables**

   * In your **Vercel Dashboard**, go to **Settings → Environment Variables**.
   * Add:

     * `TELEGRAM_BOT_TOKEN` — your Telegram bot token.
     * Any other required variables (e.g., `PINECONE_API_KEY`, `OPENAI_API_KEY`, etc.).

5. **Deploy to Vercel**

   * Push your project to **GitHub**.
   * Import the repo into **Vercel**.
   * Vercel automatically builds and deploys your app.

6. **Set Up the Webhook**

   * After deployment, set your webhook to your Vercel app’s URL:
   (how? in terminal, add curl to the following address)
   (where is ur vercel url? just click on the deployed version of the vercel and copy the provided url)

     ```bash
     https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/setWebhook?url=https://<your-vercel-app>.vercel.app/webhook
     ```
   * Replace `<TELEGRAM_BOT_TOKEN>` and `<your-vercel-app>` accordingly.

7. **Test Your Bot**

   * Send a message to your bot in Telegram.
   * Check logs in Vercel dashboard (**Deployments → Logs**) if needed.

