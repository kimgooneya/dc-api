from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, Dict, Any
from app.services.scraper import ScraperService
from app.utils.cache import SimpleCache
from app.core.config import settings
import requests

router = APIRouter()

# Initialize cache and scraper service
cache = SimpleCache(settings.CACHE_DURATION)
scraper_service = ScraperService()

@router.get("/posts", summary="Get posts from a DC Inside gallery")
async def get_gallery_posts(
    id: str = Query(..., description="Gallery identifier (e.g., 'mabinogimobile')"),
    page: int = Query(1, description="Page number"),
    list_num: int = Query(50, description="Number of posts per page"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    print(f"Fetching posts for gallery: {id}, page: {page}, list_num: {list_num}, use_cache: {use_cache}")
    try:
        cache_key = cache.generate_key("posts", id=id, page=page, list_num=list_num)
        
        # Check cache first if enabled
        if use_cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
        
        # Fetch new data
        result = scraper_service.get_gallery_posts(id, page, list_num)
        
        # Update cache
        cache.set(cache_key, result)
        
        return result
    except requests.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Failed to connect to DC Inside. The service might be down."
        )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to fetch data from DC Inside: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/info", summary="Get information about a DC Inside gallery")
async def get_gallery_info(
    id: str = Query(..., description="Gallery identifier (e.g., 'mabinogimobile')"),
    use_cache: bool = Query(True, description="Use cached results if available")
):
    try:
        # Check cache first if enabled
        if use_cache:
            cache_key = cache.generate_key("info", id=id)
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
        
        # Fetch new data
        result = scraper_service.get_gallery_info(id)
        
        # Update cache
        cache_key = cache.generate_key("info", id=id)
        cache.set(cache_key, result)
        
        return result
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")