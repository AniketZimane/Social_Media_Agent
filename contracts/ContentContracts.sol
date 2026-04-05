// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title ContentRegistry
 * @dev Smart contract for registering AI-generated content ownership
 */
contract ContentRegistry is Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    struct ContentRecord {
        string contentHash;
        string ipfsHash;
        string title;
        address creator;
        uint256 timestamp;
        string platform;
        uint256 wordCount;
        uint256 engagementScore;
        string licenseType;
        bool verified;
    }
    
    mapping(string => ContentRecord) public contentRegistry;
    mapping(address => string[]) public creatorContent;
    mapping(string => bool) public contentExists;
    
    Counters.Counter private _contentCounter;
    
    event ContentRegistered(
        string indexed contentHash,
        address indexed creator,
        string title,
        uint256 timestamp
    );
    
    event ContentVerified(string indexed contentHash, address verifier);
    
    /**
     * @dev Register new content on blockchain
     */
    function registerContent(
        string memory _contentHash,
        string memory _ipfsHash,
        string memory _title,
        string memory _platform,
        uint256 _wordCount,
        uint256 _engagementScore,
        string memory _licenseType
    ) external nonReentrant {
        require(!contentExists[_contentHash], "Content already registered");
        require(bytes(_contentHash).length > 0, "Content hash required");
        require(bytes(_title).length > 0, "Title required");
        
        ContentRecord memory newContent = ContentRecord({
            contentHash: _contentHash,
            ipfsHash: _ipfsHash,
            title: _title,
            creator: msg.sender,
            timestamp: block.timestamp,
            platform: _platform,
            wordCount: _wordCount,
            engagementScore: _engagementScore,
            licenseType: _licenseType,
            verified: true
        });
        
        contentRegistry[_contentHash] = newContent;
        creatorContent[msg.sender].push(_contentHash);
        contentExists[_contentHash] = true;
        _contentCounter.increment();
        
        emit ContentRegistered(_contentHash, msg.sender, _title, block.timestamp);
    }
    
    /**
     * @dev Verify content authenticity
     */
    function verifyContent(string memory _contentHash) 
        external 
        view 
        returns (ContentRecord memory) 
    {
        require(contentExists[_contentHash], "Content not found");
        return contentRegistry[_contentHash];
    }
    
    /**
     * @dev Get creator's content count
     */
    function getCreatorContentCount(address _creator) 
        external 
        view 
        returns (uint256) 
    {
        return creatorContent[_creator].length;
    }
    
    /**
     * @dev Get total registered content count
     */
    function getTotalContentCount() external view returns (uint256) {
        return _contentCounter.current();
    }
    
    /**
     * @dev Get creator's content hashes
     */
    function getCreatorContent(address _creator) 
        external 
        view 
        returns (string[] memory) 
    {
        return creatorContent[_creator];
    }
}

/**
 * @title BlogContentNFT
 * @dev NFT contract for AI-generated blog content
 */
contract BlogContentNFT is ERC721, ERC721URIStorage, Ownable, ReentrancyGuard {
    using Counters for Counters.Counter;
    
    Counters.Counter private _tokenIdCounter;
    
    struct NFTMetadata {
        string contentHash;
        string ipfsHash;
        address creator;
        uint256 mintedAt;
        string platform;
        uint256 royaltyPercentage;
        bool aiGenerated;
    }
    
    mapping(uint256 => NFTMetadata) public nftMetadata;
    mapping(string => uint256) public contentHashToTokenId;
    mapping(address => uint256[]) public creatorTokens;
    
    // Royalty info (EIP-2981)
    mapping(uint256 => address) private _royaltyRecipients;
    mapping(uint256 => uint256) private _royaltyPercentages;
    
    event NFTMinted(
        uint256 indexed tokenId,
        address indexed creator,
        string contentHash,
        string tokenURI
    );
    
    constructor() ERC721("AI Blog Content NFT", "AIBLOG") {}
    
    /**
     * @dev Mint NFT for blog content
     */
    function mintContentNFT(
        address _to,
        string memory _tokenURI,
        string memory _contentHash,
        string memory _ipfsHash,
        string memory _platform,
        uint256 _royaltyPercentage
    ) external nonReentrant returns (uint256) {
        require(_royaltyPercentage <= 1000, "Royalty too high"); // Max 10%
        require(contentHashToTokenId[_contentHash] == 0, "NFT already exists for this content");
        
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        
        _safeMint(_to, tokenId);
        _setTokenURI(tokenId, _tokenURI);
        
        NFTMetadata memory metadata = NFTMetadata({
            contentHash: _contentHash,
            ipfsHash: _ipfsHash,
            creator: _to,
            mintedAt: block.timestamp,
            platform: _platform,
            royaltyPercentage: _royaltyPercentage,
            aiGenerated: true
        });
        
        nftMetadata[tokenId] = metadata;
        contentHashToTokenId[_contentHash] = tokenId;
        creatorTokens[_to].push(tokenId);
        
        // Set royalty info
        _royaltyRecipients[tokenId] = _to;
        _royaltyPercentages[tokenId] = _royaltyPercentage;
        
        emit NFTMinted(tokenId, _to, _contentHash, _tokenURI);
        
        return tokenId;
    }
    
    /**
     * @dev Get NFT metadata
     */
    function getNFTMetadata(uint256 _tokenId) 
        external 
        view 
        returns (NFTMetadata memory) 
    {
        require(_exists(_tokenId), "Token does not exist");
        return nftMetadata[_tokenId];
    }
    
    /**
     * @dev Get creator's token count
     */
    function getCreatorTokenCount(address _creator) 
        external 
        view 
        returns (uint256) 
    {
        return creatorTokens[_creator].length;
    }
    
    /**
     * @dev Get creator's tokens
     */
    function getCreatorTokens(address _creator) 
        external 
        view 
        returns (uint256[] memory) 
    {
        return creatorTokens[_creator];
    }
    
    /**
     * @dev Royalty info (EIP-2981)
     */
    function royaltyInfo(uint256 _tokenId, uint256 _salePrice)
        external
        view
        returns (address, uint256)
    {
        require(_exists(_tokenId), "Token does not exist");
        
        address recipient = _royaltyRecipients[_tokenId];
        uint256 royaltyAmount = (_salePrice * _royaltyPercentages[_tokenId]) / 10000;
        
        return (recipient, royaltyAmount);
    }
    
    /**
     * @dev Check if contract supports interface
     */
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    /**
     * @dev Override tokenURI function
     */
    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
    
    /**
     * @dev Override _burn function
     */
    function _burn(uint256 tokenId) 
        internal 
        override(ERC721, ERC721URIStorage) 
    {
        super._burn(tokenId);
    }
}