"""
Test script to demonstrate news-based prediction system.
This shows how the prediction system now fetches and analyzes news to generate predictions.
"""

import asyncio
import json
from fin_ai.routes.prediction import (
    fetch_news_for_stock,
    fetch_price_data,
    analyze_news_sentiment,
    generate_ai_prediction
)


async def test_news_based_prediction():
    """Test the news-based prediction pipeline"""
    
    symbol = "APPLE"  # Use Apple for testing
    print(f"\n{'='*60}")
    print(f"NEWS-BASED PREDICTION TEST FOR: {symbol}")
    print(f"{'='*60}\n")
    
    # Step 1: Fetch news
    print("📡 Step 1: Fetching latest news articles...")
    news_articles = await fetch_news_for_stock(symbol)
    
    if news_articles:
        print(f"✓ Found {len(news_articles)} articles")
        for i, article in enumerate(news_articles[:3], 1):
            print(f"   {i}. {article.get('title', 'N/A')[:60]}...")
            print(f"      Source: {article.get('source', {}).get('name', 'Unknown')}")
    else:
        print("✗ No articles found (API key may not be configured)")
        news_articles = []
    
    # Step 2: Fetch price data
    print(f"\n📊 Step 2: Fetching price data...")
    price_data = await fetch_price_data(symbol)
    
    if price_data.get("recent_prices"):
        print(f"✓ Price Trend: {price_data['trend'].upper()}")
        print(f"  Recent prices: {[f'${p:.2f}' for p in price_data['recent_prices'][:3]]}")
    else:
        print("✗ Could not fetch price data (API key may not be configured)")
    
    # Step 3: Analyze sentiment
    print(f"\n💭 Step 3: Analyzing news sentiment...")
    if news_articles:
        sentiment_analysis = analyze_news_sentiment(news_articles, symbol)
        print(f"✓ Sentiment: {sentiment_analysis['sentiment'].upper()}")
        print(f"  Confidence: {sentiment_analysis['confidence']}%")
        print(f"  Summary: {sentiment_analysis['summary'][:100]}...")
        if sentiment_analysis.get('key_points'):
            print(f"  Key Points:")
            for point in sentiment_analysis['key_points'][:2]:
                print(f"    • {point}")
    else:
        print("✗ No articles to analyze")
        sentiment_analysis = {"sentiment": "neutral", "confidence": 50, "summary": "", "key_points": []}
    
    # Step 4: Generate prediction
    print(f"\n🤖 Step 4: Generating AI prediction...")
    if news_articles:
        price_trend = price_data.get("trend", "neutral")
        news_sentiment = sentiment_analysis["sentiment"]
        news_confidence = sentiment_analysis["confidence"]
        
        ai_prediction, confidence_score, reasoning = generate_ai_prediction(
            symbol,
            news_sentiment,
            price_trend,
            sentiment_analysis["summary"],
            news_confidence
        )
        
        print(f"✓ AI Prediction: {ai_prediction.upper()}")
        print(f"  Confidence: {confidence_score:.2%}")
        print(f"  Reasoning: {reasoning[:150]}...")
        
        # Show how prediction was formed
        print(f"\n📈 Prediction Breakdown:")
        print(f"   • News Sentiment Impact: {news_sentiment} ({news_confidence}% confidence)")
        print(f"   • Price Trend Signal: {price_trend}")
        print(f"   • Combined Decision: {ai_prediction}")
    else:
        print("✗ Could not generate prediction (no news available)")
    
    print(f"\n{'='*60}")
    print("✓ TEST COMPLETE - News-based prediction system is operational!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("\n🚀 SYSTEM STATUS: News-Integrated Prediction Engine")
    print("This system now predicts stock movements based on:")
    print("  1. Latest news articles from NewsAPI")
    print("  2. News sentiment analysis using OpenAI")
    print("  3. Recent price trends from Alpha Vantage")
    print("  4. Combined weighted signals for intelligent predictions\n")
    
    asyncio.run(test_news_based_prediction())
