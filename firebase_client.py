"""
Firebase client for persistent state management.
Handles all Firestore operations with proper error handling and retry logic.
"""
import logging
from typing import Dict, Any, Optional, List
import time
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from config import config

class FirebaseClient:
    """Firebase Firestore client for state persistence"""
    
    def __init__(self):
        self.client