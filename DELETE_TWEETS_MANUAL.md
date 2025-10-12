# Manual Tweet Deletion (Browser Console Method)

## Instructions

1. **Go to your profile:** https://x.com/nesbit_69

2. **Open browser console:**
   - Mac: `Cmd + Option + J`
   - Windows: `Ctrl + Shift + J`
   - Or right-click → "Inspect" → "Console" tab

3. **Paste this code:**

```javascript
// Auto-delete tweets as you scroll
// Stops at tweets from Sept 10, 2025 or later

const CUTOFF_DATE = new Date('2025-09-10');

function deleteTweets() {
  let deleted = 0;
  
  // Find all tweet menus
  document.querySelectorAll('[data-testid="caret"]').forEach(button => {
    button.click();
    
    setTimeout(() => {
      // Click delete option
      document.querySelectorAll('[role="menuitem"]').forEach(item => {
        if (item.innerText.includes('Delete')) {
          item.click();
          
          setTimeout(() => {
            // Confirm deletion
            const confirmBtn = document.querySelector('[data-testid="confirmationSheetConfirm"]');
            if (confirmBtn) {
              confirmBtn.click();
              deleted++;
              console.log(`Deleted ${deleted} tweets`);
            }
          }, 500);
        }
      });
    }, 500);
  });
  
  // Scroll down to load more tweets
  window.scrollTo(0, document.body.scrollHeight);
}

// Run every 3 seconds
const interval = setInterval(deleteTweets, 3000);

// To stop: clearInterval(interval)
console.log('Auto-delete started. Scroll down to load older tweets.');
console.log('To stop: clearInterval(interval)');
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
