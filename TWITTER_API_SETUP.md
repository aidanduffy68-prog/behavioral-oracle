# How to Set Up Twitter API for Bulk Delete

## Step 1: Get Twitter Developer Account

1. Go to: https://developer.twitter.com/en/portal/dashboard
2. Sign in with your Twitter account (@nesbit_69)
3. Click "Sign up for Free Account" (if you don't have one)
4. Fill out the form:
   - **What's your use case?** Select "Making a bot"
   - **Will you make Twitter content available to government?** No
   - **Describe your use case:** "Personal automation to manage my own tweets"
5. Accept terms and submit

## Step 2: Create an App

1. Once approved, click "Create App"
2. Name it something like "Tweet Cleanup Tool"
3. Click "Complete"

## Step 3: Get Your API Keys

1. Go to your app's "Keys and tokens" tab
2. You'll see:
   - **API Key** (also called Consumer Key)
   - **API Secret** (also called Consumer Secret)
3. Click "Generate" under "Access Token and Secret"
4. You'll get:
   - **Access Token**
   - **Access Token Secret**

⚠️ **Save these somewhere safe!** You can't see them again.

## Step 4: Set Permissions

1. Go to "Settings" tab
2. Under "App permissions", click "Edit"
3. Select **"Read and Write"** (you need write to delete)
4. Save

## Step 5: Add Keys to Script

Open `delete_old_tweets.py` and fill in:

```python
API_KEY = "your_api_key_here"              # From step 3
API_SECRET = "your_api_secret_here"        # From step 3
ACCESS_TOKEN = "your_access_token_here"    # From step 3
ACCESS_TOKEN_SECRET = "your_access_token_secret_here"  # From step 3
```

## Step 6: Install Dependencies

```bash
pip install tweepy
```

## Step 7: Run the Script

```bash
python delete_old_tweets.py
```

The script will:
1. Authenticate with Twitter
2. Fetch all tweets before Sept 10, 2025
3. Show you how many it found
4. Ask for confirmation
5. Delete them (with progress updates)

## Troubleshooting

**"Authentication failed"**
- Double-check your API keys
- Make sure app permissions are "Read and Write"

**"Rate limit exceeded"**
- Script automatically waits for rate limits
- If it stops, just run it again later

**"Can't fetch more than 3200 tweets"**
- Twitter API limitation
- Run the script multiple times if needed
- Each run deletes the most recent 3200 old tweets

## Notes

- Script deletes tweets in batches of ~300 per 15 minutes (Twitter limit)
- Takes ~0.5 seconds per tweet to avoid rate limits
- For 1000 tweets: ~8-10 minutes
- All deletions are permanent (can't undo)

## After You're Done

You can:
- Revoke app access: https://twitter.com/settings/connected_apps
- Delete the app from developer portal
- Delete the script and API keys
