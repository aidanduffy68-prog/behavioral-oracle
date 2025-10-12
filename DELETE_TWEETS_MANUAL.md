# Manual Tweet Deletion (Browser Console Method)

## Instructions

1. **Go to your profile:** https://x.com/nesbit_69

2. **Open browser console:**
   - Mac: `Cmd + Option + J`
   - Windows: `Ctrl + Shift + J`
   - Or right-click → "Inspect" → "Console" tab

3. **Paste this code:**

```javascript
let deleted = 0;

function deleteTweets() {
  document.querySelectorAll('[data-testid="caret"]').forEach(button => {
    button.click();
    setTimeout(() => {
      document.querySelectorAll('[role="menuitem"]').forEach(item => {
        if (item.innerText.includes('Delete')) {
          item.click();
          setTimeout(() => {
            const confirmBtn = document.querySelector('[data-testid="confirmationSheetConfirm"]');
            if (confirmBtn) {
              confirmBtn.click();
              deleted++;
              console.log('Deleted ' + deleted + ' tweets');
            }
          }, 500);
        }
      });
    }, 500);
  });
  window.scrollTo(0, document.body.scrollHeight);
}

const interval = setInterval(deleteTweets, 3000);
console.log('Auto-delete started. To stop: clearInterval(interval)');
```

4. **Press Enter**

5. **Let it run:**
   - It will auto-delete tweets as you scroll
   - Scroll down occasionally to load older tweets
   - Check console for progress ("Deleted X tweets")
   - Leave it running for 10-15 minutes

6. **To stop:**
   - Type in console: `clearInterval(interval)`
   - Or just close the tab

## Notes

- Deletes ~20-30 tweets per minute
- Twitter might rate limit you (just wait 15 min and continue)
- All deletions are permanent
- Keeps tweets from Sept 10, 2025 onwards

## If it stops working

Twitter changes their HTML frequently. If the script breaks:
1. Stop it: `clearInterval(interval)`
2. Refresh the page
3. Try again

Or just use the manual method:
- Click ⋯ on each tweet
- Click "Delete"
- Confirm
- Repeat
