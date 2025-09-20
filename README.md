# Culinary-ai-boardgame
A Python board game where players build a food empire on a square grid by acquiring restaurants, managing capital, and navigating chance events. The goal is to grow portfolio value and outmaneuver rivals to become the leading culinary tycoon.

Features
- Board rendering: Prints a square board with coordinates and stacked symbols for multiple items per cell
- Data ingestion: Parses a CSV of restaurant listings into a position→restaurant map with headers, prices, and types
- Core models: RestaurantManager (capital, buy logic, portfolio display, loss handling, next-move calculation) and Restaurant (type, price, shared ownership)
- Special grids: Abstract grid effects with StartGrid (+200 BiteCoins) and ChanceGrid (random reward, penalty, or transport)
- Game loop: Board setup, manager creation, movement options, purchasing, capital updates, and win-condition checks
