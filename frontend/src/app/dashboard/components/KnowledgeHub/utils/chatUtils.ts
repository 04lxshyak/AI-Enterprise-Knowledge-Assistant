/**
 * Counts the user's total queries from chat history.
 */
export function countChatQueries(): number {
  try {
    const chatHistory = localStorage.getItem("chat_history");
    if (!chatHistory) return 0;
    
    const history = JSON.parse(chatHistory);
    // Count only user messages (queries).
    return history.filter((msg: any) => msg.sender === "user").length;
  } catch {
    return 0;
  }
}

/**
 * Calculates the average confidence across all assistant responses.
 */
export function calculateAverageConfidence(): number {
  try {
    const chatHistory = localStorage.getItem("chat_history");
    if (!chatHistory) return 0;
    
    const history = JSON.parse(chatHistory);
    
    // Keep only assistant messages with confidence or sources that include confidence.
    const assistantMessages = history.filter((msg: any) => msg.sender === "assistant");
    
    if (assistantMessages.length === 0) return 0;
    
    const confidences: number[] = [];
    
    assistantMessages.forEach((msg: any) => {
      // Skip messages that say "I don't have that information".
      if (msg.content?.toLowerCase().includes("i don't have that information")) {
        return;
      }
      
      // Find the best confidence value, matching ChatMessage.
      if (msg.sources && msg.sources.length > 0) {
        const sourceConfidences = msg.sources
          .map((src: any) => src.confidence)
          .filter((conf: any) => typeof conf === "number");
        
        if (sourceConfidences.length > 0) {
          confidences.push(Math.max(...sourceConfidences));
          return;
        }
      }
      
      // If there are no sources with confidence, use the message confidence.
      if (typeof msg.confidence === "number") {
        confidences.push(msg.confidence);
      }
    });
    
    if (confidences.length === 0) return 0;
    
    const average = confidences.reduce((sum, conf) => sum + conf, 0) / confidences.length;
    return Math.round(average * 10) / 10; // Round to 1 decimal place.
  } catch {
    return 0;
  }
}

/**
 * Formats a large number with thousands separators.
 */
export function formatNumber(num: number): string {
  return num.toLocaleString();
}
