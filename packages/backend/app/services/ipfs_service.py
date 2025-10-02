"""IPFS storage service using Pinata."""

from typing import Any, BinaryIO

import httpx

from app.core.config import settings


class IPFSService:
    """Service for storing files on IPFS via Pinata."""

    def __init__(self) -> None:
        """Initialize Pinata client."""
        self.base_url = "https://api.pinata.cloud"
        self.gateway_url = "https://gateway.pinata.cloud/ipfs"
        self.headers = {
            "Authorization": f"Bearer {settings.PINATA_JWT}",
        }

    async def upload_file(
        self, file: BinaryIO, filename: str, metadata: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Upload a file to IPFS via Pinata."""
        url = f"{self.base_url}/pinning/pinFileToIPFS"

        files = {"file": (filename, file)}

        data = {}
        if metadata:
            data["pinataMetadata"] = str(metadata)

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                url, headers=self.headers, files=files, data=data
            )
            response.raise_for_status()
            result = response.json()

        return {
            "cid": result["IpfsHash"],
            "size": result["PinSize"],
            "timestamp": result["Timestamp"],
            "url": f"{self.gateway_url}/{result['IpfsHash']}",
        }

    async def upload_json(self, data: dict[str, Any], name: str) -> dict[str, Any]:
        """Upload JSON data to IPFS via Pinata."""
        url = f"{self.base_url}/pinning/pinJSONToIPFS"

        payload = {
            "pinataContent": data,
            "pinataMetadata": {"name": name},
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()

        return {
            "cid": result["IpfsHash"],
            "size": result["PinSize"],
            "timestamp": result["Timestamp"],
            "url": f"{self.gateway_url}/{result['IpfsHash']}",
        }

    async def get_file_info(self, cid: str) -> dict[str, Any]:
        """Get information about a pinned file."""
        url = f"{self.base_url}/data/pinList"
        params = {"hashContains": cid}

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            result = response.json()

        if result["count"] > 0:
            pin_data = result["rows"][0]
            return {
                "cid": pin_data["ipfs_pin_hash"],
                "size": pin_data["size"],
                "timestamp": pin_data["date_pinned"],
                "name": pin_data.get("metadata", {}).get("name", ""),
            }

        raise ValueError(f"File with CID {cid} not found")

    async def unpin_file(self, cid: str) -> bool:
        """Unpin a file from IPFS (soft delete)."""
        url = f"{self.base_url}/pinning/unpin/{cid}"

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.delete(url, headers=self.headers)
            response.raise_for_status()

        return True

    def get_file_url(self, cid: str) -> str:
        """Get the gateway URL for a file."""
        return f"{self.gateway_url}/{cid}"


ipfs_service = IPFSService()
