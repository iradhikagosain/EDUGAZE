import requests
import base64
from datetime import datetime, timedelta
from django.conf import settings
import json

class ZoomAPI:
    def __init__(self):
        self.client_id = getattr(settings, 'a3NZdgiyRXKKCgLO9ukn2A', '')
        self.client_secret = getattr(settings, 'U89jT0wGpAxfrZoSgiJqk4ptsOmO0St8', '')
        self.account_id = getattr(settings, 'qMaPzx2-Rsi1pl5SXAYkzA', '')
        self.base_url = "https://api.zoom.us/v2"
        self.access_token = None
        self.token_expiry = None
    
    def get_access_token(self):
        """Get OAuth access token for Server-to-Server app"""
       
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
    
        auth_str = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            'Authorization': f'Basic {auth_str}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'account_credentials',
            'account_id': self.account_id
        }
        
        try:
            response = requests.post(
                'https://zoom.us/oauth/token',
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data['access_token']
                # Set expiry 50 minutes from now (tokens last 1 hour)
                self.token_expiry = datetime.now() + timedelta(minutes=50)
                print("Zoom API: Successfully obtained access token")
                return self.access_token
            else:
                print(f"Zoom OAuth Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Zoom OAuth Exception: {str(e)}")
            return None
    
    def create_meeting(self, topic, start_time, duration=60, password=None):
        """Create a Zoom meeting"""
        access_token = self.get_access_token()
        if not access_token:
            print("Zoom API: Failed to get access token")
            return None
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Format start time for Zoom API
        start_time_iso = start_time.strftime("%Y-%m-%dT%H:%M:%S")
        
        data = {
            "topic": topic,
            "type": 2,  # Scheduled meeting
            "start_time": start_time_iso,
            "duration": duration,
            "timezone": "UTC",
            "password": password or "123456",
            "settings": {
                "host_video": True,
                "participant_video": True,
                "join_before_host": False,
                "mute_upon_entry": False,
                "waiting_room": False,
                "auto_recording": "none",
                "enforce_login": False
            }
        }
        
        try:
            print(f"Zoom API: Creating meeting - {topic} at {start_time_iso}")
            response = requests.post(
                f"{self.base_url}/users/me/meetings",
                headers=headers,
                data=json.dumps(data)
            )
            
            if response.status_code == 201:
                meeting_data = response.json()
                print(f"Zoom API: Meeting created successfully - ID: {meeting_data['id']}")
                return {
                    'meeting_id': str(meeting_data['id']),
                    'join_url': meeting_data['join_url'],
                    'start_url': meeting_data['start_url'],
                    'password': meeting_data['password']
                }
            else:
                print(f"Zoom API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Zoom API Exception: {str(e)}")
            return None
    
    def get_meeting(self, meeting_id):
        """Get meeting details"""
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/meetings/{meeting_id}",
                headers=headers
            )
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error getting meeting: {str(e)}")
            return None