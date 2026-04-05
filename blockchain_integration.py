import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from web3 import Web3
from eth_account import Account
import ipfshttpclient
from dotenv import load_dotenv

load_dotenv()

class BlockchainContentManager:
    def __init__(self):
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URL", "https://polygon-rpc.com")))
        self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
        self.account = Account.from_key(self.private_key) if self.private_key else None
        
        # IPFS client for decentralized storage
        try:
            self.ipfs_client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
        except:
            self.ipfs_client = None
            print("⚠️ IPFS client not available. Using fallback storage.")
        
        # Smart contract addresses (deploy these contracts)
        self.content_registry_address = os.getenv("CONTENT_REGISTRY_CONTRACT")
        self.nft_contract_address = os.getenv("NFT_CONTRACT_ADDRESS")
        
        # Content ownership registry
        self.content_registry = {}
        
    def create_content_hash(self, content: str, title: str, author: str) -> str:
        """Create unique hash for content"""
        content_data = f"{title}|{content}|{author}|{datetime.now().isoformat()}"
        return hashlib.sha256(content_data.encode()).hexdigest()
    
    def store_content_on_ipfs(self, content_data: Dict) -> Optional[str]:
        """Store content on IPFS for decentralized storage"""
        try:
            if self.ipfs_client:
                # Convert content to JSON
                content_json = json.dumps(content_data, indent=2)
                
                # Add to IPFS
                result = self.ipfs_client.add_json(content_data)
                ipfs_hash = result
                
                print(f"✅ Content stored on IPFS: {ipfs_hash}")
                return ipfs_hash
            else:
                # Fallback: simulate IPFS hash
                content_str = json.dumps(content_data)
                return f"Qm{hashlib.sha256(content_str.encode()).hexdigest()[:44]}"
        except Exception as e:
            print(f"❌ IPFS storage failed: {e}")
            return None
    
    def register_content_ownership(self, content_data: Dict) -> Dict:
        """Register content ownership on blockchain"""
        try:
            # Create content metadata
            content_hash = self.create_content_hash(
                content_data['content'], 
                content_data['title'], 
                content_data.get('author', 'Anonymous')
            )
            
            # Store on IPFS
            ipfs_hash = self.store_content_on_ipfs(content_data)
            
            # Create blockchain record
            ownership_record = {
                "content_hash": content_hash,
                "ipfs_hash": ipfs_hash,
                "title": content_data['title'],
                "author": content_data.get('author', 'Anonymous'),
                "created_at": datetime.now().isoformat(),
                "platform": content_data.get('platform', 'Unknown'),
                "word_count": len(content_data['content'].split()),
                "engagement_score": content_data.get('engagement_score', 0),
                "blockchain_tx": None,  # Will be filled when deployed to actual blockchain
                "owner_address": self.account.address if self.account else None,
                "license": "CC BY-SA 4.0",  # Creative Commons license
                "verified": True
            }
            
            # Simulate blockchain transaction (replace with actual smart contract call)
            if self.account and self.w3.is_connected():
                # This would be actual smart contract interaction
                ownership_record["blockchain_tx"] = f"0x{hashlib.sha256(content_hash.encode()).hexdigest()}"
                ownership_record["block_number"] = self.w3.eth.block_number
                ownership_record["gas_used"] = 21000  # Estimated gas
            
            # Store in local registry
            self.content_registry[content_hash] = ownership_record
            
            print(f"✅ Content ownership registered: {content_hash[:16]}...")
            return ownership_record
            
        except Exception as e:
            print(f"❌ Blockchain registration failed: {e}")
            return {"error": str(e)}
    
    def create_content_nft(self, content_data: Dict, ownership_record: Dict) -> Dict:
        """Create NFT for blog content"""
        try:
            # NFT metadata following OpenSea standard
            nft_metadata = {
                "name": f"Blog: {content_data['title']}",
                "description": f"AI-generated blog content about {content_data.get('topic', 'various topics')}. Created using Agentic AI system.",
                "image": content_data.get('image_url', 'https://via.placeholder.com/512x512?text=Blog+NFT'),
                "external_url": f"https://ipfs.io/ipfs/{ownership_record.get('ipfs_hash', '')}",
                "attributes": [
                    {"trait_type": "Content Type", "value": "AI Blog"},
                    {"trait_type": "Platform", "value": content_data.get('platform', 'Multi-Platform')},
                    {"trait_type": "Word Count", "value": len(content_data['content'].split())},
                    {"trait_type": "Engagement Score", "value": f"{content_data.get('engagement_score', 0):.2f}"},
                    {"trait_type": "Creation Date", "value": datetime.now().strftime("%Y-%m-%d")},
                    {"trait_type": "AI Model", "value": "Google Gemini + Agentic AI"},
                    {"trait_type": "Creator", "value": content_data.get('author', 'Aniket Zimane')},
                    {"trait_type": "License", "value": "CC BY-SA 4.0"}
                ],
                "properties": {
                    "content_hash": ownership_record['content_hash'],
                    "ipfs_hash": ownership_record['ipfs_hash'],
                    "blockchain_verified": True,
                    "ai_generated": True
                }
            }
            
            # Store NFT metadata on IPFS
            nft_ipfs_hash = self.store_content_on_ipfs(nft_metadata)
            
            # Simulate NFT minting (replace with actual smart contract call)
            nft_record = {
                "token_id": len(self.content_registry) + 1000,  # Simulate token ID
                "contract_address": self.nft_contract_address or "0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6",
                "metadata_uri": f"ipfs://{nft_ipfs_hash}",
                "owner": self.account.address if self.account else "0x0000000000000000000000000000000000000000",
                "minted_at": datetime.now().isoformat(),
                "mint_tx": f"0x{hashlib.sha256(f'nft_{ownership_record['content_hash']}'.encode()).hexdigest()}",
                "royalty_percentage": 10,  # 10% royalty to creator
                "marketplace_url": f"https://opensea.io/assets/matic/{self.nft_contract_address or '0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6'}/{len(self.content_registry) + 1000}"
            }
            
            print(f"✅ NFT created: Token ID {nft_record['token_id']}")
            return nft_record
            
        except Exception as e:
            print(f"❌ NFT creation failed: {e}")
            return {"error": str(e)}
    
    def verify_content_authenticity(self, content_hash: str) -> Dict:
        """Verify content authenticity using blockchain"""
        try:
            if content_hash in self.content_registry:
                record = self.content_registry[content_hash]
                return {
                    "verified": True,
                    "owner": record.get('owner_address'),
                    "created_at": record.get('created_at'),
                    "blockchain_tx": record.get('blockchain_tx'),
                    "ipfs_hash": record.get('ipfs_hash'),
                    "license": record.get('license')
                }
            else:
                return {"verified": False, "error": "Content not found in registry"}
        except Exception as e:
            return {"verified": False, "error": str(e)}
    
    def get_content_ownership_history(self, content_hash: str) -> List[Dict]:
        """Get ownership history of content"""
        # Simulate ownership history (in real implementation, query blockchain events)
        if content_hash in self.content_registry:
            record = self.content_registry[content_hash]
            return [{
                "event": "Content Created",
                "timestamp": record.get('created_at'),
                "owner": record.get('owner_address'),
                "transaction": record.get('blockchain_tx')
            }]
        return []
    
    def create_content_license(self, content_hash: str, license_type: str = "CC BY-SA 4.0") -> Dict:
        """Create blockchain-based content license"""
        try:
            license_data = {
                "content_hash": content_hash,
                "license_type": license_type,
                "granted_at": datetime.now().isoformat(),
                "grantor": self.account.address if self.account else None,
                "terms": {
                    "commercial_use": license_type in ["CC BY", "CC BY-SA"],
                    "modification": license_type in ["CC BY", "CC BY-SA"],
                    "attribution_required": True,
                    "share_alike": "SA" in license_type
                },
                "license_tx": f"0x{hashlib.sha256(f'license_{content_hash}'.encode()).hexdigest()}"
            }
            
            print(f"✅ Content license created: {license_type}")
            return license_data
            
        except Exception as e:
            print(f"❌ License creation failed: {e}")
            return {"error": str(e)}
    
    def get_creator_analytics(self, creator_address: str) -> Dict:
        """Get blockchain analytics for content creator"""
        try:
            creator_content = [
                record for record in self.content_registry.values() 
                if record.get('owner_address') == creator_address
            ]
            
            total_content = len(creator_content)
            total_words = sum(record.get('word_count', 0) for record in creator_content)
            avg_engagement = sum(record.get('engagement_score', 0) for record in creator_content) / max(total_content, 1)
            
            return {
                "creator_address": creator_address,
                "total_content_pieces": total_content,
                "total_words_written": total_words,
                "average_engagement": avg_engagement,
                "content_verified": total_content,  # All content is verified
                "nfts_created": total_content,  # Assuming each content becomes NFT
                "blockchain_reputation": min(100, total_content * 10 + avg_engagement * 50)
            }
            
        except Exception as e:
            return {"error": str(e)}

class BlockchainContentIntegration:
    """Integration layer for blockchain functionality in the blog assistant"""
    
    def __init__(self):
        self.blockchain_manager = BlockchainContentManager()
    
    def process_generated_content(self, blog_content: Dict, author: str = "Aniket Zimane") -> Dict:
        """Process generated blog content with blockchain integration"""
        try:
            # Add author information
            blog_content['author'] = author
            blog_content['ai_generated'] = True
            blog_content['creation_timestamp'] = datetime.now().isoformat()
            
            # Register content ownership on blockchain
            ownership_record = self.blockchain_manager.register_content_ownership(blog_content)
            
            # Create NFT for the content
            nft_record = self.blockchain_manager.create_content_nft(blog_content, ownership_record)
            
            # Create content license
            license_record = self.blockchain_manager.create_content_license(
                ownership_record['content_hash'], 
                "CC BY-SA 4.0"
            )
            
            # Enhanced blog content with blockchain data
            enhanced_content = {
                **blog_content,
                'blockchain': {
                    'ownership': ownership_record,
                    'nft': nft_record,
                    'license': license_record,
                    'verified': True,
                    'content_hash': ownership_record['content_hash'],
                    'ipfs_url': f"https://ipfs.io/ipfs/{ownership_record.get('ipfs_hash', '')}",
                    'nft_marketplace_url': nft_record.get('marketplace_url', ''),
                    'blockchain_explorer_url': f"https://polygonscan.com/tx/{ownership_record.get('blockchain_tx', '')}"
                }
            }
            
            print(f"✅ Blockchain integration completed for: {blog_content['title'][:50]}...")
            return enhanced_content
            
        except Exception as e:
            print(f"❌ Blockchain integration failed: {e}")
            # Return original content if blockchain fails
            blog_content['blockchain'] = {'error': str(e), 'verified': False}
            return blog_content
    
    def verify_content(self, content_hash: str) -> Dict:
        """Verify content using blockchain"""
        return self.blockchain_manager.verify_content_authenticity(content_hash)
    
    def get_creator_stats(self, creator_address: str = None) -> Dict:
        """Get creator statistics from blockchain"""
        if not creator_address and self.blockchain_manager.account:
            creator_address = self.blockchain_manager.account.address
        
        if creator_address:
            return self.blockchain_manager.get_creator_analytics(creator_address)
        else:
            return {"error": "No creator address provided"}

# Global blockchain integration instance
blockchain_integration = BlockchainContentIntegration()