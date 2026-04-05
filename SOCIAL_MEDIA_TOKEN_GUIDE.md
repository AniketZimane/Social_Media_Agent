# Social Media API Token Setup Guide

## 📘 LinkedIn Access Token

### Method 1: LinkedIn Developer Portal (Recommended)
1. Go to https://www.linkedin.com/developers/apps
2. Click "Create app"
3. Fill in:
   - App name: "My Blog Poster"
   - LinkedIn Page: Select your page (create one if needed)
   - App logo: Upload any image
4. Click "Create app"
5. Go to "Auth" tab
6. Add redirect URL: `http://localhost:5000/callback`
7. Under "OAuth 2.0 scopes", request:
   - `w_member_social` (Share content on behalf of user)
   - `r_liteprofile` (Read profile)
8. Copy your **Client ID** and **Client Secret**
9. Generate token using OAuth 2.0 flow:
   ```
   https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:5000/callback&scope=w_member_social%20r_liteprofile
   ```
10. After authorization, exchange code for access token

### Method 2: Quick Test Token (Expires in 60 days)
1. Go to https://www.linkedin.com/developers/apps
2. Select your app → "Auth" tab
3. Scroll to "OAuth 2.0 tools"
4. Click "Generate token"
5. Copy the access token

---

## 👥 Facebook/Instagram Access Token

### For Facebook Pages:
1. Go to https://developers.facebook.com/
2. Click "My Apps" → "Create App"
3. Select "Business" type
4. Fill in app details
5. Add "Facebook Login" product
6. Go to Tools → Graph API Explorer
7. Select your app
8. Select "User Token" → Get Token → "Get Page Access Token"
9. Select your page
10. Copy the **Page Access Token**
11. To make it permanent:
    - Go to https://developers.facebook.com/tools/debug/accesstoken/
    - Paste your token
    - Click "Extend Access Token"

### For Instagram:
1. Connect Instagram to Facebook Page
2. Use Facebook Graph API with Instagram permissions
3. Required permissions: `instagram_basic`, `instagram_content_publish`

---

## 🐦 Twitter (X) API Token

### Twitter API v2:
1. Go to https://developer.twitter.com/
2. Sign up for Developer Account
3. Create a new Project and App
4. Go to "Keys and tokens" tab
5. Generate:
   - **API Key** (Consumer Key)
   - **API Secret** (Consumer Secret)
   - **Bearer Token**
   - **Access Token**
   - **Access Token Secret**
6. Save all tokens securely

### Required Permissions:
- Read and Write tweets
- Read users

---

## 🔐 How to Add Tokens to Your App

1. Open `.env` file in your project
2. Add your tokens:

```env
# LinkedIn
LINKEDIN_ACCESS_TOKEN=your_linkedin_token_here

# Facebook
FACEBOOK_ACCESS_TOKEN=your_facebook_page_token_here
FACEBOOK_PAGE_ID=your_facebook_page_id_here

# Twitter
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
TWITTER_API_KEY=your_twitter_api_key_here
TWITTER_API_SECRET=your_twitter_api_secret_here
TWITTER_ACCESS_TOKEN=your_twitter_access_token_here
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret_here

# Instagram (uses Facebook Graph API)
INSTAGRAM_ACCESS_TOKEN=your_instagram_token_here
INSTAGRAM_BUSINESS_ACCOUNT_ID=your_instagram_business_id_here
```

3. Restart your Flask server

---

## ⚠️ Important Notes

### Token Security:
- Never commit `.env` file to Git
- Keep tokens private
- Rotate tokens regularly
- Use environment variables in production

### Token Expiration:
- **LinkedIn**: 60 days (need to refresh)
- **Facebook**: Can be permanent if extended
- **Twitter**: Permanent until revoked
- **Instagram**: Same as Facebook

### Rate Limits:
- **LinkedIn**: 100 posts per day
- **Facebook**: Varies by app review status
- **Twitter**: 300 tweets per 3 hours
- **Instagram**: 25 posts per day

---

## 🧪 Testing Your Tokens

Run this Python script to test:

```python
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Test LinkedIn
linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
if linkedin_token:
    response = requests.get(
        "https://api.linkedin.com/v2/me",
        headers={"Authorization": f"Bearer {linkedin_token}"}
    )
    print(f"LinkedIn: {response.status_code}")

# Test Facebook
facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
if facebook_token:
    response = requests.get(
        f"https://graph.facebook.com/me?access_token={facebook_token}"
    )
    print(f"Facebook: {response.status_code}")

# Test Twitter
twitter_bearer = os.getenv("TWITTER_BEARER_TOKEN")
if twitter_bearer:
    response = requests.get(
        "https://api.twitter.com/2/users/me",
        headers={"Authorization": f"Bearer {twitter_bearer}"}
    )
    print(f"Twitter: {response.status_code}")
```

---

## 📚 Additional Resources

- LinkedIn API Docs: https://docs.microsoft.com/en-us/linkedin/
- Facebook Graph API: https://developers.facebook.com/docs/graph-api
- Twitter API Docs: https://developer.twitter.com/en/docs
- Instagram API: https://developers.facebook.com/docs/instagram-api

---

## 🆘 Troubleshooting

### "Invalid Token" Error:
- Check token hasn't expired
- Verify correct permissions/scopes
- Ensure token is for correct account

### "Rate Limit Exceeded":
- Wait for rate limit reset
- Implement exponential backoff
- Consider upgrading API tier

### "Permission Denied":
- Request additional scopes
- Complete app review process
- Verify account permissions
