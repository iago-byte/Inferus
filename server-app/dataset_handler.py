from __future__ import annotations

"""Dataset utilities for training and inference.

This module introduces a simple registry and abstraction layer so different
 datasets can be configured from a central place. A dataset handler is
responsible for building a :class:`~torch.utils.data.Dataset` and exposing a
:class:`~torch.utils.data.DataLoader` ready for consumption by a model
handler.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Type

from torch.utils.data import DataLoader, Dataset
from torchvision import transforms as T
from PIL import Image


class BasicDatasetHandler(ABC):
    """Base class for dataset configuration."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def build(self) -> Dataset:
        """Create and return the dataset object."""

    def dataloader(self, shuffle: bool = True) -> DataLoader:
        """Utility to wrap the dataset in a dataloader."""
        dataset = self.build()
        batch_size = int(self.config.get("batch_size", 1))
        num_workers = int(self.config.get("num_workers", 0))
        return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)


_DATASET_REGISTRY: Dict[str, Type[BasicDatasetHandler]] = {}


def register_dataset(name: str) -> Any:
    """Class decorator to register dataset handlers."""

    def decorator(cls: Type[BasicDatasetHandler]) -> Type[BasicDatasetHandler]:
        _DATASET_REGISTRY[name] = cls
        return cls

    return decorator


def create_dataset_handler(name: str, config: Dict[str, Any]) -> BasicDatasetHandler:
    """Factory helper to instantiate dataset handlers."""
    if name not in _DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset handler: {name}")
    return _DATASET_REGISTRY[name](config)


class SimpleSegmentationDataset(Dataset):
    """Toy dataset reading images and masks from folders."""

    def __init__(self, img_dir: str, mask_dir: str, transform: T.Compose | None = None):
        self.img_dir = Path(img_dir)
        self.mask_dir = Path(mask_dir)
        self.transform = transform
        self._images = sorted(self.img_dir.glob("*.png"))

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._images)

    def __getitem__(self, idx: int):
        img_path = self._images[idx]
        mask_path = self.mask_dir / img_path.name
        image = Image.open(img_path).convert("RGB")
        mask = Image.open(mask_path)
        if self.transform:
            image = self.transform(image)
            mask = T.PILToTensor()(mask)
        return image, mask.long()


@register_dataset("segmentation")
class SegmentationDatasetHandler(BasicDatasetHandler):
    """Handler for simple image segmentation datasets."""

    def build(self) -> Dataset:
        img_dir = self.config["images"]
        mask_dir = self.config["masks"]
        transform = T.Compose([
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        return SimpleSegmentationDataset(img_dir, mask_dir, transform)