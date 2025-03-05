# Caching System

The Botwell framework implements a robust caching system to improve performance and reduce API costs.

## How It Works

The caching system functions by:

1. Generating a unique cache key for each API request based on:
   - The model ID
   - The prompt text
   - Any other relevant parameters

2. Storing API responses in JSON files in the `.cache/` directory

3. Retrieving cached responses for identical requests instead of making new API calls

4. Automatically invalidating cached responses after a configurable time period (default: 7 days)

## Benefits

The caching system provides several key benefits:

- **Cost Reduction**: Significant API cost savings by reusing responses for identical prompts
- **Development Speed**: Faster development and testing cycles
- **Consistency**: More consistent results when running multiple tests
- **Reduced API Load**: Fewer redundant API calls to model providers

## Implementation

The system is implemented in `botwell/utils/caching.py` with the following key components:

```python
# Cache decorator that can be applied to API functions
@cache_response
def call_api(model_id, prompt, temperature=0.7):
    # API call implementation
    ...
```

## Cache Management

The framework includes tools for managing the cache:

```bash
# View cache statistics
botwell cache stats

# Clear expired cache entries
botwell cache clear --expired-only

# Clear all cache entries
botwell cache clear
```

## Example Cache Statistics

```
Cache Statistics:
----------------
Total entries: 1,324
Total size: 28.7 MB
Oldest entry: 2025-02-01 09:23:45
Newest entry: 2025-03-01 14:38:12
Expired entries: 72
Active entries: 1,252
Hit rate (last run): 87.3%
```

## Technical Details

1. **Cache Key Generation**: MD5 hash of model ID and prompt
2. **Cache Entry Format**:
   ```json
   {
     "model": "anthropic/claude-3-opus",
     "prompt": "...",
     "response": "...",
     "timestamp": "2025-02-28T15:42:37",
     "expires": "2025-03-07T15:42:37"
   }
   ```
3. **Expiration Logic**: Each entry contains an expiration time
4. **Cache Validation**: Before returning a cached result, the system checks:
   - If the cache file exists
   - If the entry hasn't expired
   - If the entry is valid and complete

## Configuration

The caching system can be configured through environment variables:

```bash
# Set cache expiration time (in days)
export BOTWELL_CACHE_EXPIRATION=14

# Disable caching entirely
export BOTWELL_DISABLE_CACHE=1
```