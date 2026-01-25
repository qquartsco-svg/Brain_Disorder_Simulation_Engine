"""
ADHD Simulation Engine - Setup Script

GitHub 배포를 위한 패키지 설정
"""

from setuptools import setup, find_packages
from pathlib import Path

# README 읽기
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

# requirements.txt 읽기
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip() 
            for line in f 
            if line.strip() and not line.startswith('#')
        ]

setup(
    name="adhd-simulation-engine",
    version="1.0.0",
    author="GNJz",
    author_email="",  # 필요시 추가
    description="Cookiie Brain Engine 기반 ADHD 전용 시뮬레이션 시스템",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qquartsco-svg/ADHD_Simulation_Engine",
    packages=find_packages(exclude=['tests', 'docs', 'examples', '*.tests', '*.tests.*', 'tests.*']),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
        "full": [
            "scipy>=1.7.0",
            "pandas>=1.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "adhd-simulate=cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.yaml", "*.yml"],
    },
    keywords="adhd simulation cognitive neuroscience research education",
    project_urls={
        "Bug Reports": "https://github.com/qquartsco-svg/ADHD_Simulation_Engine/issues",
        "Source": "https://github.com/qquartsco-svg/ADHD_Simulation_Engine",
        "Documentation": "https://github.com/qquartsco-svg/ADHD_Simulation_Engine#readme",
    },
)

