from __future__ import annotations

from .types import DocCategory


CLASSIFY_INSTRUCTION = (
    "You are a precise document classifier with expertise in business documents and digital content. "
    "Analyze the provided image or PDF and classify it into exactly one of these categories: "
    "1) 'invoice' - Bills, receipts, payment documents with amounts and vendor information "
    "2) 'marketplace_listing_screenshot' - Product listings from platforms like eBay, Facebook Marketplace, Craigslist "
    "3) 'chat_screenshot' - Messaging conversations from any chat application "
    "4) 'website_screenshot' - Web page captures showing website content "
    "5) 'other' - Any document that doesn't clearly fit the above categories. "
    "Consider visual layout, text content, and contextual clues. Provide a confidence score (0.0-1.0). "
    "Return ONLY valid JSON matching the provided schema."
)


EXTRACTION_INSTRUCTIONS_CATEGORY = {
    DocCategory.INVOICE: (
        "You are an expert invoice data extractor. Carefully analyze this invoice document and extract all available information. "
        "Look for: invoice number (any reference/ID numbers), invoice date (when issued), total amount (final sum to pay), "
        "detailed description, quantity and price of each items/services, vendor/company name (who issued the invoice), and any address information. "
        "Be precise with numbers and dates. If information is not clearly visible, use null. "
        "Also extract the complete raw text content via OCR. Return ONLY valid JSON matching the schema."
    ),
    DocCategory.MARKETPLACE_LISTING_SCREENSHOT: (
        "You are an expert marketplace listing analyzer. Extract comprehensive information from this listing screenshot. "
        "Identify: the listing title, price (with currency if visible), location/area, all item characteristics and features mentioned, "
        "full item description, and seller name/username. Look carefully for condition, size, brand, model, or any specifications. "
        "Capture all descriptive text that helps understand what's being sold. "
        "Also extract the complete raw text content via OCR. Return ONLY valid JSON matching the schema."
    ),
    DocCategory.CHAT_SCREENSHOT: (
        "You are an expert chat conversation analyzer. Extract detailed information from this chat screenshot. "
        "Identify: all participants/usernames involved, any visible timestamps, and structure each message with sender, text content, and time. "
        "Preserve the conversation flow and capture all visible text messages. Pay attention to profile names, display names, and message timestamps. "
        "Extract every message bubble visible in the screenshot, maintaining chronological order when possible. "
        "Also extract the complete raw text content via OCR. Return ONLY valid JSON matching the schema."
    ),
    DocCategory.WEBSITE_SCREENSHOT: (
        "You are an expert website content analyzer. Extract key information from this website screenshot. "
        "Identify: the website URL (if visible in address bar), page title, and determine the website type (e.g., e-commerce, blog, news, corporate, social media). "
        "Look for navigation elements, headers, main content areas, and any identifying features that indicate the site's purpose. "
        "Capture key textual content that defines what this webpage is about. "
        "Also extract the complete raw text content via OCR. Return ONLY valid JSON matching the schema."
    ),
    DocCategory.OTHER: (
        "You are an expert document analyzer for uncategorized content. Since this document doesn't fit standard categories, "
        "perform comprehensive analysis to extract all available information. "
        "Look for: any identifying numbers or codes, dates, names of people or organizations, amounts or quantities, "
        "document type indicators (forms, certificates, reports, etc.), key headings or sections, "
        "contact information (addresses, phone numbers, emails), and any structured data present. "
        "Identify the apparent purpose or nature of the document. Extract all readable text, tables, lists, and data fields. "
        "Pay attention to logos, letterheads, signatures, stamps, or official markings that might indicate document authority or source. "
        "Capture any metadata visible (creation dates, file properties, etc.). "
        "Also extract the complete raw text content via OCR. Return ONLY valid JSON matching the schema."
    ),
}
