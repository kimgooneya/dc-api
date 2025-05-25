import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
from app.core.config import settings

class ScraperService:
    def __init__(self):
        self.headers = {
            "User-Agent": settings.DEFAULT_USER_AGENT
        }
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> str:
        """Make an HTTP request to the target site"""
        response = requests.get(url, params=params, headers=self.headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.text
    
    def get_gallery_posts(self, gallery_id: str, page: int, list_num: int) -> Dict[str, Any]:
        """Scrape posts from a DC Inside gallery"""
        params = {
            "id": gallery_id,
            "page": page,
            "list_num": list_num
        }
        
        html = self._make_request(settings.DC_BASE_URL, params)
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract gallery info
        gallery_info = self._extract_gallery_info(soup)
        
        # Extract posts
        posts = self._extract_posts(soup)
        
        # Build the result
        return {
            "gallery_info": gallery_info,
            "posts": posts,
            "meta": {
                "page": page,
                "list_num": list_num,
                "gallery_id": gallery_id,
                "post_count": len(posts)
            }
        }
    
    def get_gallery_info(self, gallery_id: str) -> Dict[str, Any]:
        """Scrape information about a DC Inside gallery"""
        params = {"id": gallery_id}
        
        html = self._make_request(settings.DC_BASE_URL, params)
        soup = BeautifulSoup(html, 'html.parser')
        
        return self._extract_gallery_info(soup, detailed=True)
    
    def _extract_gallery_info(self, soup: BeautifulSoup, detailed: bool = False) -> Dict[str, Any]:
        """Extract gallery information from the parsed HTML"""
        gallery_info = {}
        
        # Extract basic gallery info
        gallery_info["title"] = soup.select_one(".gallname").text.strip() if soup.select_one(".gallname") else None
        
        manager_info = soup.select(".gall-info .manager-info")
        gallery_info["managers"] = [m.text.strip() for m in manager_info if m] if manager_info else []
        
        creation_date = soup.select_one(".gall-info .creation-date")
        gallery_info["creation_date"] = creation_date.text.strip() if creation_date else None
        
        if detailed:
            # Extract additional info for detailed view
            description = soup.select_one(".gallery_info .txt")
            gallery_info["description"] = description.text.strip() if description else None
            
            related_galleries = []
            related_section = soup.select(".related_link a")
            for rel in related_section:
                related_galleries.append({
                    "name": rel.text.strip(),
                    "url": rel["href"] if "href" in rel.attrs else None
                })
            gallery_info["related_galleries"] = related_galleries
        
        return gallery_info
    
    def _extract_posts(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract posts from the parsed HTML"""
        posts = []
        post_rows = soup.select(".gall_list .us-post")
        
        for row in post_rows:
            post = {}
            
            # Extract post number
            num_cell = row.select_one(".gall_num")
            post["number"] = num_cell.text.strip() if num_cell else None
            
            # Skip notice posts if needed
            if post["number"] and post["number"] in ["공지", "설문"]:
                continue
                
            # Extract post title
            title_element = row.select_one(".gall_tit a:first-child")
            post["title"] = title_element.text.strip() if title_element else None
            post["url"] = title_element["href"] if title_element and "href" in title_element.attrs else None
            
            # Extract reply count
            reply_count = row.select_one(".gall_tit .reply_num")
            post["reply_count"] = reply_count.text.strip('[]') if reply_count else "0"
            
            # Extract author info
            author_element = row.select_one(".gall_writer")
            if author_element:
                post["author"] = {
                    "name": author_element.get("data-nick", ""),
                    "id": author_element.get("data-uid", ""),
                    "ip": author_element.get("data-ip", "")
                }
            
            # Extract date and time
            date_element = row.select_one(".gall_date")
            post["date"] = date_element.get("title", "") if date_element else ""
            post["timestamp"] = date_element.text.strip() if date_element else ""
            
            # Extract view count
            view_element = row.select_one(".gall_count")
            post["views"] = view_element.text.strip() if view_element else "0"
            
            # Extract recommendation count
            recommend_element = row.select_one(".gall_recommend")
            post["recommends"] = recommend_element.text.strip() if recommend_element else "0"
            
            posts.append(post)
        
        return posts 