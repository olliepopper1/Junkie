/**
 * Discord Integration Script
 * Handles Discord client ID integration and dynamic link generation
 */

document.addEventListener('DOMContentLoaded', function() {
  // Fetch Discord client ID from the API
  fetch('/api/discord-client-id')
    .then(response => response.json())
    .then(data => {
      // Get the Add to Discord button
      const addToDiscordBtn = document.querySelector('a[href*="discord.com/api/oauth2/authorize"]');
      
      if (addToDiscordBtn && data.client_id) {
        // Update the href with the actual client ID
        const originalHref = addToDiscordBtn.getAttribute('href');
        const newHref = originalHref.replace('1234567890123456789', data.client_id);
        addToDiscordBtn.setAttribute('href', newHref);
        
        // Enable the button (in case it was disabled)
        addToDiscordBtn.classList.remove('disabled');
      }
    })
    .catch(error => {
      console.error('Error fetching Discord client ID:', error);
      
      // Disable the Add to Discord button if there's an error
      const addToDiscordBtn = document.querySelector('a[href*="discord.com/api/oauth2/authorize"]');
      if (addToDiscordBtn) {
        addToDiscordBtn.classList.add('disabled');
        addToDiscordBtn.setAttribute('title', 'Unable to load Discord integration');
      }
    });
});