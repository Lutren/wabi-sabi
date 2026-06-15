#!/usr/bin/env python3
"""
MEDIOEVO Text Processor
Removes AI-like patterns and em-dashes from text files
"""

import re
import sys
import os
from pathlib import Path

def remove_ai_patterns(text):
    """Remove common AI-generated text patterns"""
    # Common AI phrases to remove or replace
    ai_patterns = [
        (r'\b(It is important to note|It should be noted|It is worth noting)\b', ''),
        (r'\b(In conclusion|In summary|To summarize|In short)\b', ''),
        (r'\b(Futhermore|Moreover|Additionally|Besides)\b', ''),
        (r'\b(It is clear that|It is evident that|It is obvious that)\b', ''),
        (r'\b(One can see|One can observe|One can notice)\b', ''),
        (r'\b(As mentioned earlier|As stated before|As previously discussed)\b', ''),
        (r'\b(This shows that|This demonstrates that|This illustrates that)\b', ''),
        (r'\b(In today\'s world|In modern society|In the current era)\b', ''),
        (r'\b(It goes without saying|Needless to say|Obviously)\b', ''),
        (r'\b(When it comes to|When dealing with|Regarding)\b', ''),
        (r'\b(There is no doubt that|Undoubtedly|Without a doubt)\b', ''),
    ]
    
    result = text
    for pattern, replacement in ai_patterns:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    
    # Clean up extra spaces
    result = re.sub(r'\s+', ' ', result)
    result = re.sub(r'\s+([,.!?;:])', r'\1', result)
    
    return result.strip()

def remove_em_dashes(text):
    """Replace em-dashes and en-dashes with regular hyphens"""
    # Replace em-dash ( — ) and en-dash ( – ) with regular hyphen
    text = re.sub(r'[—–]', '-', text)
    # Replace spaces around dashes with single space
    text = re.sub(r'\s*-\s*', ' - ', text)
    # Clean up multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_file(input_path, output_path=None):
    """Process a single file"""
    if output_path is None:
        output_path = input_path
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process the content
        content = remove_ai_patterns(content)
        content = remove_em_dashes(content)
        
        # Write back
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Processed: {input_path}")
        return True
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False

def process_directory(directory_path, extensions=None):
    """Process all files in a directory with given extensions"""
    if extensions is None:
        extensions = ['.md', '.txt', '.html', '.htm', '.css', '.js', '.ts']
    
    processed = 0
    errors = 0
    
    for ext in extensions:
        for file_path in Path(directory_path).rglob(f'*{ext}'):
            if process_file(file_path):
                processed += 1
            else:
                errors += 1
    
    print(f"\nProcessed {processed} files, {errors} errors")
    return processed, errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python text_processor.py <file_or_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        process_file(path)
    elif os.path.isdir(path):
        process_directory(path)
    else:
        print(f"Path not found: {path}")
        sys.exit(1)