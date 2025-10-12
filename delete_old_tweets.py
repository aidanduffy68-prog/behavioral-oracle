#!/usr/bin/env python3
"""
Delete all tweets before September 10, 2025
Twitter: @nesbit_69
"""

import tweepy
from datetime import datetime
import time

# ============================================
# SETUP INSTRUCTIONS:
# ============================================
# 1. Go to https://developer.twitter.com/en/portal/dashboard
# 2. Create a new app (or use existing)
# 3. Get your API keys from the "Keys and tokens" tab
# 4. Fill in the values below
# ============================================

# YOUR API CREDENTIALS (fill these in)
API_KEY = "your_api_key_here"
API_SECRET = "your_api_secret_here"
ACCESS_TOKEN = "your_access_token_here"
ACCESS_TOKEN_SECRET = "your_access_token_secret_here"

# Cutoff date: Delete everything BEFORE this date
CUTOFF_DATE = datetime(2025, 9, 10, 0, 0, 0)

def authenticate():
    """Authenticate with Twitter API"""
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    
    # Verify credentials
    try:
        api.verify_credentials()
        print("✓ Authentication successful")
        return api
    except Exception as e:
        print(f"✗ Authentication failed: {e}")
        return None

def get_tweets_to_delete(api):
    """Fetch all tweets before cutoff date"""
    tweets_to_delete = []
    
    print(f"\nFetching tweets before {CUTOFF_DATE.strftime('%Y-%m-%d')}...")
    
    try:
        # Fetch tweets (Twitter API returns max 3200 recent tweets)
        for tweet in tweepy.Cursor(api.user_timeline, 
                                   tweet_mode='extended',
                                   count=200).items():
            
            # Check if tweet is before cutoff date
            if tweet.created_at < CUTOFF_DATE:
                tweets_to_delete.append(tweet)
                
            # Progress indicator
            if len(tweets_to_delete) % 100 == 0:
                print(f"  Found {len(tweets_to_delete)} tweets to delete...")
                
    except Exception as e:
        print(f"Error fetching tweets: {e}")
    
    return tweets_to_delete

def delete_tweets(api, tweets):
    """Delete the specified tweets"""
    if not tweets:
        print("\n✓ No tweets found before cutoff date")
        return
    
    print(f"\n⚠️  Found {len(tweets)} tweets to delete")
    print(f"   Oldest: {tweets[-1].created_at.strftime('%Y-%m-%d')}")
    print(f"   Newest: {tweets[0].created_at.strftime('%Y-%m-%d')}")
    
    # Confirm deletion
    response = input(f"\nDelete {len(tweets)} tweets? (yes/no): ")
    if response.lower() != 'yes':
        print("Cancelled.")
        return
    
    print("\nDeleting tweets...")
    deleted_count = 0
    failed_count = 0
    
    for i, tweet in enumerate(tweets, 1):
        try:
            api.destroy_status(tweet.id)
            deleted_count += 1
            
            # Progress update every 10 tweets
            if i % 10 == 0:
                print(f"  Deleted {deleted_count}/{len(tweets)} tweets...")
            
            # Rate limiting: Twitter allows ~300 deletes per 15 min
            # Sleep briefly to avoid hitting limits
            time.sleep(0.5)
            
        except Exception as e:
            failed_count += 1
            print(f"  Failed to delete tweet {tweet.id}: {e}")
    
    print(f"\n✓ Deletion complete!")
    print(f"  Deleted: {deleted_count}")
    print(f"  Failed: {failed_count}")

def main():
    print("=" * 50)
    print("Twitter Bulk Delete Script")
    print("Delete all tweets before September 10, 2025")
    print("=" * 50)
    
    # Authenticate
    api = authenticate()
    if not api:
        print("\n⚠️  Please add your API credentials to the script")
        return
    
    # Get tweets to delete
    tweets = get_tweets_to_delete(api)
    
    # Delete tweets
    delete_tweets(api, tweets)

if __name__ == "__main__":
    main()
