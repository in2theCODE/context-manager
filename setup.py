from setuptools import setup, find_packages

setup(
    name='context_manager',  # Changed from context-manager to match Python naming
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'gitpython>=3.1.30',
        'pyyaml>=6.0',
        'jinja2>=3.1.2',
        'rich>=13.3.3',
        'typer>=0.7.0',
        'anthropic>=0.7.0',
        'python-dotenv>=1.0.0'
    ],
    extras_require={
        'ml': [
            'transformers>=4.30.0',
            'sentence-transformers>=2.2.0',
            'scikit-learn>=1.2.0'
        ]
    },
    entry_points={
        'console_scripts': [
            'context-manager=context_manager.cli:main',
        ],
    },
    python_requires='>=3.10',
)
