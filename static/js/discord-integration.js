/**
 * Discord Integration Script
 * Handles Discord client ID integration and dynamic link generation
 */

document.addEventListener('DOMContentLoaded', function() {
  // Find all Discord bot invite links that need dynamic client ID
  const discordInviteLinks = document.querySelectorAll('.discord-bot-invite');
  
  if (discordInviteLinks.length > 0) {
    // Fetch the client ID from the API
    fetch('/api/discord-client-id')
      .then(response => response.json())
      .then(data => {
        const clientId = data.client_id;
        
        // Update all Discord invite links with the correct client ID
        discordInviteLinks.forEach(link => {
          const baseUrl = "https://discord.com/api/oauth2/authorize";
          const permissions = link.getAttribute('data-permissions') || '8';
          const scope = link.getAttribute('data-scope') || 'bot%20applications.commands';
          
          const inviteUrl = `${baseUrl}?client_id=${clientId}&permissions=${permissions}&scope=${scope}`;
          link.href = inviteUrl;
        });
      })
      .catch(error => {
        console.error('Error fetching Discord client ID:', error);
      });
  }
});