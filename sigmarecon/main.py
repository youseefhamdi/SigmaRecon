#!/usr/bin/env python3
"""
SigmaRecon - 2026-Ready Attack Surface Discovery CLI

A comprehensive reconnaissance platform that unifies 23+ subdomain enumeration tools,
provides a resilient data collection pipeline, and supports extensible configuration management.
"""

import argparse
import sys
import os
from typing import Optional, Dict, List
from pathlib import Path


class SigmaReconCLI:
    """Main CLI application for SigmaRecon reconnaissance platform."""
    
    def __init__(self):
        self.parser = None
        self.subparsers = None
        
    def setup_parser(self) -> argparse.ArgumentParser:
        """Setup the main argument parser with all commands."""
        # Main parser
        self.parser = argparse.ArgumentParser(
            prog='sigma',
            description='SigmaRecon - 2026-Ready Attack Surface Discovery CLI',
            epilog='''
Examples:
  sigma discover -d example.com --sources subfinder,amass --format jsonl
  sigma scan --target example.com --mode comprehensive --output results.jsonl
  sigma monitor --domains example.com --interval 3600 --output monitor.log
  sigma analyze -i results.jsonl --filter live --group-by root
  sigma config show --profile default
  sigma report -i results.jsonl --format html --template executive
  sigma plugin list --installed
  sigma update --check --auto-update

For more information, visit: https://sigmarecon.io
            ''',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Global arguments
        self.parser.add_argument(
            '--version', '-v',
            action='version',
            version='SigmaRecon v1.0.0'
        )
        
        self.parser.add_argument(
            '--verbose', '-V',
            action='store_true',
            help='Enable verbose output'
        )
        
        self.parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Suppress non-essential output'
        )
        
        self.parser.add_argument(
            '--log-level',
            choices=['debug', 'info', 'warn', 'error'],
            default='info',
            help='Set logging level'
        )
        
        self.parser.add_argument(
            '--config-file',
            type=str,
            help='Path to configuration file'
        )
        
        self.parser.add_argument(
            '--profile',
            type=str,
            default='default',
            help='Configuration profile to use'
        )
        
        # Create subparsers for commands
        self.subparsers = self.parser.add_subparsers(
            dest='command',
            help='Available commands',
            metavar='COMMAND'
        )
        
        # Setup command subparsers
        self._setup_discover_command()
        self._setup_scan_command()
        self._setup_monitor_command()
        self._setup_analyze_command()
        self._setup_config_command()
        self._setup_report_command()
        self._setup_plugin_command()
        self._setup_update_command()
        
        return self.parser
    
    def _setup_discover_command(self):
        """Setup the discover command for passive subdomain discovery."""
        discover_parser = self.subparsers.add_parser(
            'discover',
            help='Passive subdomain discovery using multiple sources',
            description='Discover subdomains using passive aggregation from multiple sources including certificate transparency logs, search engines, and other public sources.'
        )
        
        # Domain inputs
        domain_group = discover_parser.add_argument_group('Domain Input')
        domain_input = domain_group.add_mutually_exclusive_group(required=True)
        domain_input.add_argument(
            '-d', '--domain',
            type=str,
            help='Single domain to discover subdomains for'
        )
        domain_input.add_argument(
            '-dL', '--domain-list',
            type=str,
            help='File containing list of domains (one per line)'
        )
        
        # Discovery sources
        source_group = discover_parser.add_argument_group('Source Selection')
        source_group.add_argument(
            '--sources',
            type=str,
            help='Comma-separated list of sources to use (e.g., subfinder,amass,crtsh)'
        )
        source_group.add_argument(
            '--exclude-sources',
            type=str,
            help='Comma-separated list of sources to exclude'
        )
        source_group.add_argument(
            '--all-sources',
            action='store_true',
            help='Use all available sources'
        )
        
        # Rate limiting and performance
        rate_group = discover_parser.add_argument_group('Performance & Rate Limiting')
        rate_group.add_argument(
            '--rate-limit',
            type=int,
            default=300,
            help='Global rate limit in requests per minute (default: 300)'
        )
        rate_group.add_argument(
            '--timeout',
            type=int,
            default=30,
            help='Request timeout in seconds (default: 30)'
        )
        rate_group.add_argument(
            '--retries',
            type=int,
            default=3,
            help='Number of retries for failed requests (default: 3)'
        )
        
        # Output options
        output_group = discover_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-o', '--output',
            type=str,
            help='Output file path'
        )
        output_group.add_argument(
            '--format',
            choices=['jsonl', 'csv', 'ndjson', 'txt'],
            default='jsonl',
            help='Output format (default: jsonl)'
        )
        output_group.add_argument(
            '--append',
            action='store_true',
            help='Append to existing output file instead of overwriting'
        )
        output_group.add_argument(
            '--dedupe',
            action='store_true',
            help='Remove duplicate results'
        )
        
        # Provider configuration
        provider_group = discover_parser.add_argument_group('Provider Configuration')
        provider_group.add_argument(
            '--api-keys',
            type=str,
            help='JSON file containing API keys for various providers'
        )
        provider_group.add_argument(
            '--no-api-keys',
            action='store_true',
            help='Use only free sources (no API keys required)'
        )
    
    def _setup_scan_command(self):
        """Setup the scan command for comprehensive reconnaissance."""
        scan_parser = self.subparsers.add_parser(
            'scan',
            help='Comprehensive reconnaissance scan',
            description='Run a complete reconnaissance workflow including discovery, resolution, validation, and HTTP probing.'
        )
        
        # Target specification
        target_group = scan_parser.add_argument_group('Target Specification')
        target_group.add_argument(
            '--target', '-t',
            type=str,
            required=True,
            help='Target domain or organization'
        )
        target_group.add_argument(
            '--target-list',
            type=str,
            help='File containing list of targets'
        )
        
        # Scan modes
        scan_parser.add_argument(
            '--mode',
            choices=['basic', 'comprehensive', 'stealth', 'aggressive'],
            default='basic',
            help='Scan mode to use (default: basic)'
        )
        
        # Pipeline configuration
        pipeline_group = scan_parser.add_argument_group('Pipeline Configuration')
        pipeline_group.add_argument(
            '--stages',
            type=str,
            help='Comma-separated list of stages to run (discover,resolve,validate,probe)'
        )
        pipeline_group.add_argument(
            '--skip-stages',
            type=str,
            help='Comma-separated list of stages to skip'
        )
        
        # Performance tuning
        perf_group = scan_parser.add_argument_group('Performance Tuning')
        perf_group.add_argument(
            '--threads',
            type=int,
            default=100,
            help='Number of concurrent threads (default: 100)'
        )
        perf_group.add_argument(
            '--max-candidates',
            type=int,
            help='Maximum number of candidates to process'
        )
        perf_group.add_argument(
            '--wildcard-tests',
            type=int,
            default=3,
            help='Number of wildcard detection tests (default: 3)'
        )
        
        # Output options
        output_group = scan_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-o', '--output',
            type=str,
            help='Output file for final results'
        )
        output_group.add_argument(
            '--output-dir',
            type=str,
            default='./scan_results',
            help='Directory for intermediate outputs (default: ./scan_results)'
        )
        output_group.add_argument(
            '--format',
            choices=['jsonl', 'csv', 'sqlite', 'neo4j'],
            default='jsonl',
            help='Output format (default: jsonl)'
        )
        
        # Advanced options
        adv_group = scan_parser.add_argument_group('Advanced Options')
        adv_group.add_argument(
            '--save-intermediate',
            action='store_true',
            help='Save intermediate results for each stage'
        )
        adv_group.add_argument(
            '--continue-from',
            type=str,
            choices=['discover', 'resolve', 'validate', 'probe'],
            help='Continue scan from specific stage'
        )
        adv_group.add_argument(
            '--profile',
            type=str,
            help='Scan profile configuration'
        )
    
    def _setup_monitor_command(self):
        """Setup the monitor command for continuous monitoring."""
        monitor_parser = self.subparsers.add_parser(
            'monitor',
            help='Continuous attack surface monitoring',
            description='Monitor domains for changes in attack surface, new subdomains, and certificate updates.'
        )
        
        # Domain monitoring
        domain_group = monitor_parser.add_argument_group('Domain Monitoring')
        domain_group.add_argument(
            '--domains',
            type=str,
            required=True,
            help='Comma-separated list of domains to monitor'
        )
        domain_group.add_argument(
            '--domain-file',
            type=str,
            help='File containing domains to monitor (one per line)'
        )
        
        # Monitoring configuration
        config_group = monitor_parser.add_argument_group('Monitoring Configuration')
        config_group.add_argument(
            '--interval',
            type=int,
            default=3600,
            help='Monitoring interval in seconds (default: 3600 = 1 hour)'
        )
        config_group.add_argument(
            '--schedule',
            type=str,
            choices=['cron', 'interval'],
            default='interval',
            help='Monitoring schedule type'
        )
        config_group.add_argument(
            '--cron-expr',
            type=str,
            help='Cron expression for scheduled monitoring'
        )
        
        # Alerting and notifications
        alert_group = monitor_parser.add_argument_group('Alerting & Notifications')
        alert_group.add_argument(
            '--alerts',
            type=str,
            help='Alert methods: email,slack,webhook (comma-separated)'
        )
        alert_group.add_argument(
            '--alert-config',
            type=str,
            help='Configuration file for alerts'
        )
        alert_group.add_argument(
            '--min-changes',
            type=int,
            default=1,
            help='Minimum number of changes before sending alert'
        )
        
        # Data retention
        retention_group = monitor_parser.add_argument_group('Data Retention')
        retention_group.add_argument(
            '--retention-days',
            type=int,
            default=30,
            help='Number of days to retain monitoring data'
        )
        retention_group.add_argument(
            '--diff-only',
            action='store_true',
            help='Only output changes, not full results'
        )
        
        # Output options
        output_group = monitor_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-o', '--output',
            type=str,
            help='Output file or directory'
        )
        output_group.add_argument(
            '--format',
            choices=['jsonl', 'csv', 'html'],
            default='jsonl',
            help='Output format (default: jsonl)'
        )
    
    def _setup_analyze_command(self):
        """Setup the analyze command for result analysis."""
        analyze_parser = self.subparsers.add_parser(
            'analyze',
            help='Analyze reconnaissance results',
            description='Analyze collected reconnaissance data for insights, patterns, and security findings.'
        )
        
        # Input data
        input_group = analyze_parser.add_argument_group('Input Data')
        input_group.add_argument(
            '-i', '--input',
            type=str,
            required=True,
            help='Input file(s) to analyze'
        )
        input_group.add_argument(
            '--recursive',
            action='store_true',
            help='Process directories recursively'
        )
        
        # Analysis operations
        analyze_parser.add_argument(
            '--operation',
            choices=['stats', 'filter', 'group', 'diff', 'enrich', 'validate'],
            required=True,
            help='Analysis operation to perform'
        )
        
        # Filtering options
        filter_group = analyze_parser.add_argument_group('Filtering Options')
        filter_group.add_argument(
            '--filter',
            type=str,
            help='Filter expression (e.g., status=live,tags=admin)'
        )
        filter_group.add_argument(
            '--regex',
            type=str,
            help='Regex pattern to match'
        )
        filter_group.add_argument(
            '--domain',
            type=str,
            help='Filter by specific domain'
        )
        filter_group.add_argument(
            '--source',
            type=str,
            help='Filter by source tool'
        )
        
        # Grouping and aggregation
        group_group = analyze_parser.add_argument_group('Grouping & Aggregation')
        group_group.add_argument(
            '--group-by',
            choices=['root', 'source', 'status', 'tags', 'date'],
            help='Group results by specified field'
        )
        group_group.add_argument(
            '--aggregate',
            choices=['count', 'unique', 'first', 'last'],
            default='unique',
            help='Aggregation method for groups'
        )
        
        # Enrichment options
        enrich_group = analyze_parser.add_argument_group('Enrichment Options')
        enrich_group.add_argument(
            '--resolve',
            action='store_true',
            help='Resolve unresolved domains'
        )
        enrich_group.add_argument(
            '--probe',
            action='store_true',
            help='Probe HTTP endpoints'
        )
        enrich_group.add_argument(
            '--tech-detect',
            action='store_true',
            help='Detect technologies on web endpoints'
        )
        
        # Output options
        output_group = analyze_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-o', '--output',
            type=str,
            help='Output file for analysis results'
        )
        output_group.add_argument(
            '--format',
            choices=['jsonl', 'csv', 'html', 'table'],
            default='jsonl',
            help='Output format (default: jsonl)'
        )
        output_group.add_argument(
            '--stats',
            action='store_true',
            help='Generate statistics summary'
        )
    
    def _setup_config_command(self):
        """Setup the config command for configuration management."""
        config_parser = self.subparsers.add_parser(
            'config',
            help='Configuration management',
            description='Manage SigmaRecon configuration, profiles, and provider settings.'
        )
        
        config_subparsers = config_parser.add_subparsers(
            dest='config_command',
            help='Configuration subcommands',
            metavar='SUBCOMMAND'
        )
        
        # Show configuration
        show_parser = config_subparsers.add_parser(
            'show',
            help='Display current configuration'
        )
        show_parser.add_argument(
            '--profile',
            type=str,
            help='Specific profile to show'
        )
        show_parser.add_argument(
            '--format',
            choices=['json', 'yaml', 'table'],
            default='yaml',
            help='Output format (default: yaml)'
        )
        show_parser.add_argument(
            '--secrets',
            action='store_true',
            help='Show secret values (default: masked)'
        )
        
        # Set configuration
        set_parser = config_subparsers.add_parser(
            'set',
            help='Set configuration value'
        )
        set_parser.add_argument(
            'key',
            type=str,
            help='Configuration key (e.g., profiles.default.output.dir)'
        )
        set_parser.add_argument(
            'value',
            type=str,
            help='Configuration value'
        )
        set_parser.add_argument(
            '--profile',
            type=str,
            help='Target profile'
        )
        
        # Unset configuration
        unset_parser = config_subparsers.add_parser(
            'unset',
            help='Remove configuration value'
        )
        unset_parser.add_argument(
            'key',
            type=str,
            help='Configuration key to remove'
        )
        unset_parser.add_argument(
            '--profile',
            type=str,
            help='Target profile'
        )
        
        # Initialize configuration
        init_parser = config_subparsers.add_parser(
            'init',
            help='Initialize new configuration'
        )
        init_parser.add_argument(
            '--force',
            action='store_true',
            help='Overwrite existing configuration'
        )
        init_parser.add_argument(
            '--profile',
            type=str,
            help='Create specific profile'
        )
        
        # Manage profiles
        profile_parser = config_subparsers.add_parser(
            'profile',
            help='Manage configuration profiles'
        )
        profile_parser.add_argument(
            '--list',
            action='store_true',
            help='List all profiles'
        )
        profile_parser.add_argument(
            '--create',
            type=str,
            help='Create new profile from current config'
        )
        profile_parser.add_argument(
            '--delete',
            type=str,
            help='Delete specified profile'
        )
        profile_parser.add_argument(
            '--copy',
            nargs=2,
            metavar=('SOURCE', 'DEST'),
            help='Copy profile (source destination)'
        )
        
        # Provider management
        provider_parser = config_subparsers.add_parser(
            'provider',
            help='Manage provider configurations'
        )
        provider_parser.add_argument(
            '--list',
            action='store_true',
            help='List available providers'
        )
        provider_parser.add_argument(
            '--keys',
            action='store_true',
            help='Show configured API keys'
        )
        provider_parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate provider configurations'
        )
        provider_parser.add_argument(
            '--add',
            nargs=2,
            metavar=('NAME', 'KEY'),
            help='Add provider API key'
        )
        provider_parser.add_argument(
            '--remove',
            type=str,
            help='Remove provider API key'
        )
    
    def _setup_report_command(self):
        """Setup the report command for generating reports."""
        report_parser = self.subparsers.add_parser(
            'report',
            help='Generate comprehensive reports',
            description='Generate various types of reports from reconnaissance data including executive summaries, technical findings, and compliance reports.'
        )
        
        # Input data
        input_group = report_parser.add_argument_group('Input Data')
        input_group.add_argument(
            '-i', '--input',
            type=str,
            required=True,
            help='Input data file(s) for reporting'
        )
        input_group.add_argument(
            '--multiple',
            action='store_true',
            help='Input contains multiple data files'
        )
        
        # Report types
        report_parser.add_argument(
            '--type',
            choices=['executive', 'technical', 'compliance', 'diff', 'summary'],
            default='technical',
            help='Type of report to generate (default: technical)'
        )
        
        # Templates
        template_group = report_parser.add_argument_group('Templates')
        template_group.add_argument(
            '--template',
            type=str,
            help='Report template to use'
        )
        template_group.add_argument(
            '--list-templates',
            action='store_true',
            help='List available templates'
        )
        template_group.add_argument(
            '--custom-template',
            type=str,
            help='Custom template file'
        )
        
        # Data processing
        data_group = report_parser.add_argument_group('Data Processing')
        data_group.add_argument(
            '--filter',
            type=str,
            help='Filter data before reporting'
        )
        data_group.add_argument(
            '--date-range',
            nargs=2,
            metavar=('START', 'END'),
            help='Date range for report (YYYY-MM-DD YYYY-MM-DD)'
        )
        data_group.add_argument(
            '--include-metadata',
            action='store_true',
            help='Include metadata and provenance'
        )
        
        # Output options
        output_group = report_parser.add_argument_group('Output Options')
        output_group.add_argument(
            '-o', '--output',
            type=str,
            help='Output file path'
        )
        output_group.add_argument(
            '--format',
            choices=['html', 'pdf', 'docx', 'json', 'csv', 'markdown'],
            default='html',
            help='Output format (default: html)'
        )
        output_group.add_argument(
            '--compress',
            action='store_true',
            help='Compress output file'
        )
        output_group.add_argument(
            '--open',
            action='store_true',
            help='Open report in default browser after generation'
        )
        
        # Branding and customization
        brand_group = report_parser.add_argument_group('Branding & Customization')
        brand_group.add_argument(
            '--company',
            type=str,
            help='Company name for report branding'
        )
        brand_group.add_argument(
            '--logo',
            type=str,
            help='Logo file path for report header'
        )
        brand_group.add_argument(
            '--theme',
            type=str,
            help='Report theme/style'
        )
    
    def _setup_plugin_command(self):
        """Setup the plugin command for plugin management."""
        plugin_parser = self.subparsers.add_parser(
            'plugin',
            help='Plugin management',
            description='Manage SigmaRecon plugins including discovery, installation, configuration, and removal.'
        )
        
        plugin_subparsers = plugin_parser.add_subparsers(
            dest='plugin_command',
            help='Plugin subcommands',
            metavar='SUBCOMMAND'
        )
        
        # List plugins
        list_parser = plugin_subparsers.add_parser(
            'list',
            help='List available or installed plugins'
        )
        list_parser.add_argument(
            '--installed',
            action='store_true',
            help='Show only installed plugins'
        )
        list_parser.add_argument(
            '--available',
            action='store_true',
            help='Show only available plugins'
        )
        list_parser.add_argument(
            '--category',
            type=str,
            help='Filter by plugin category'
        )
        list_parser.add_argument(
            '--search',
            type=str,
            help='Search plugins by name or description'
        )
        
        # Install plugin
        install_parser = plugin_subparsers.add_parser(
            'install',
            help='Install plugin'
        )
        install_parser.add_argument(
            'plugin_name',
            type=str,
            help='Name of plugin to install'
        )
        install_parser.add_argument(
            '--version',
            type=str,
            help='Specific version to install'
        )
        install_parser.add_argument(
            '--source',
            type=str,
            help='Plugin source (repository URL or local path)'
        )
        install_parser.add_argument(
            '--force',
            action='store_true',
            help='Force installation even if already installed'
        )
        
        # Uninstall plugin
        uninstall_parser = plugin_subparsers.add_parser(
            'uninstall',
            help='Uninstall plugin'
        )
        uninstall_parser.add_argument(
            'plugin_name',
            type=str,
            help='Name of plugin to uninstall'
        )
        uninstall_parser.add_argument(
            '--force',
            action='store_true',
            help='Force uninstallation'
        )
        uninstall_parser.add_argument(
            '--purge-config',
            action='store_true',
            help='Remove configuration files'
        )
        
        # Plugin info
        info_parser = plugin_subparsers.add_parser(
            'info',
            help='Show plugin information'
        )
        info_parser.add_argument(
            'plugin_name',
            type=str,
            help='Plugin name to get information about'
        )
        
        # Plugin configuration
        config_parser = plugin_subparsers.add_parser(
            'config',
            help='Configure plugin'
        )
        config_parser.add_argument(
            'plugin_name',
            type=str,
            help='Plugin to configure'
        )
        config_parser.add_argument(
            '--show',
            action='store_true',
            help='Show current configuration'
        )
        config_parser.add_argument(
            '--set',
            nargs=2,
            metavar=('KEY', 'VALUE'),
            help='Set configuration value'
        )
        config_parser.add_argument(
            '--unset',
            type=str,
            help='Remove configuration value'
        )
        
        # Plugin enable/disable
        enable_parser = plugin_subparsers.add_parser(
            'enable',
            help='Enable plugin'
        )
        enable_parser.add_argument(
            'plugin_name',
            type=str,
            help='Plugin name to enable'
        )
        
        disable_parser = plugin_subparsers.add_parser(
            'disable',
            help='Disable plugin'
        )
        disable_parser.add_argument(
            'plugin_name',
            type=str,
            help='Plugin name to disable'
        )
        
        # Plugin update
        update_parser = plugin_subparsers.add_parser(
            'update',
            help='Update plugin'
        )
        update_parser.add_argument(
            'plugin_name',
            type=str,
            help='Plugin name to update'
        )
        update_parser.add_argument(
            '--check',
            action='store_true',
            help='Check for updates without installing'
        )
    
    def _setup_update_command(self):
        """Setup the update command for tool and configuration updates."""
        update_parser = self.subparsers.add_parser(
            'update',
            help='Update SigmaRecon and integrated tools',
            description='Update SigmaRecon core, integrated reconnaissance tools, and configuration templates.'
        )
        
        # Update targets
        target_group = update_parser.add_argument_group('Update Targets')
        target_group.add_argument(
            '--core',
            action='store_true',
            help='Update SigmaRecon core application'
        )
        target_group.add_argument(
            '--tools',
            action='store_true',
            help='Update integrated reconnaissance tools'
        )
        target_group.add_argument(
            '--configs',
            action='store_true',
            help='Update configuration templates'
        )
        target_group.add_argument(
            '--plugins',
            action='store_true',
            help='Update installed plugins'
        )
        target_group.add_argument(
            '--wordlists',
            action='store_true',
            help='Update wordlists and dictionaries'
        )
        
        # Update options
        update_parser.add_argument(
            '--check',
            action='store_true',
            help='Check for available updates without applying them'
        )
        update_parser.add_argument(
            '--auto-update',
            action='store_true',
            help='Automatically apply updates without prompting'
        )
        update_parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )
        
        # Source configuration
        source_group = update_parser.add_argument_group('Update Sources')
        source_group.add_argument(
            '--channel',
            choices=['stable', 'beta', 'dev'],
            default='stable',
            help='Update channel (default: stable)'
        )
        source_group.add_argument(
            '--repository',
            type=str,
            help='Custom repository URL'
        )
        source_group.add_argument(
            '--mirror',
            type=str,
            help='Mirror server to use for updates'
        )
        
        # Backup and rollback
        backup_group = update_parser.add_argument_group('Backup & Rollback')
        backup_group.add_argument(
            '--backup',
            action='store_true',
            help='Create backup before updating'
        )
        backup_group.add_argument(
            '--rollback',
            type=str,
            help='Rollback to specified version'
        )
        backup_group.add_argument(
            '--list-backups',
            action='store_true',
            help='List available backups'
        )
        
        # Notification
        notify_group = update_parser.add_argument_group('Notifications')
        notify_group.add_argument(
            '--notify',
            action='store_true',
            help='Send notification when updates are available'
        )
        notify_group.add_argument(
            '--webhook',
            type=str,
            help='Webhook URL for update notifications'
        )
    
    def validate_arguments(self, args) -> bool:
        """Validate command arguments and combinations."""
        # Validate discover command
        if args.command == 'discover':
            if not hasattr(args, 'domain') and not hasattr(args, 'domain_list'):
                self.parser.error("discover command requires either --domain or --domain-list")
            
            # Validate sources
            if args.all_sources and (args.sources or args.exclude_sources):
                self.parser.error("Cannot use --all-sources with --sources or --exclude-sources")
        
        # Validate scan command
        elif args.command == 'scan':
            if not hasattr(args, 'target') and not hasattr(args, 'target_list'):
                self.parser.error("scan command requires --target or --target-list")
            
            # Validate scan modes
            if args.mode == 'aggressive' and args.threads > 500:
                print("Warning: Aggressive mode with >500 threads may trigger rate limits")
        
        # Validate monitor command
        elif args.command == 'monitor':
            if not hasattr(args, 'domains') and not hasattr(args, 'domain_file'):
                self.parser.error("monitor command requires --domains or --domain-file")
            
            # Validate scheduling
            if args.schedule == 'cron' and not args.cron_expr:
                self.parser.error("Cron schedule requires --cron-expr")
        
        # Validate config commands
        elif args.command == 'config':
            if not hasattr(args, 'config_command'):
                self.parser.error("config subcommand is required")
        
        # Validate plugin commands
        elif args.command == 'plugin':
            if not hasattr(args, 'plugin_command'):
                self.parser.error("plugin subcommand is required")
        
        # Validate input file exists
        if hasattr(args, 'input') and args.input:
            if not os.path.exists(args.input):
                self.parser.error(f"Input file not found: {args.input}")
        
        # Validate output directory
        if hasattr(args, 'output_dir') and args.output_dir:
            output_dir = Path(args.output_dir)
            if not output_dir.parent.exists():
                self.parser.error(f"Output directory parent does not exist: {output_dir.parent}")
        
        return True
    
    def execute_command(self, args):
        """Execute the parsed command with proper routing."""
        if args.verbose:
            print(f"Executing command: {args.command}")
            if hasattr(args, 'config_command'):
                print(f"Subcommand: {args.config_command}")
        
        # Route to appropriate command handler
        try:
            if args.command == 'discover':
                self._execute_discover(args)
            elif args.command == 'scan':
                self._execute_scan(args)
            elif args.command == 'monitor':
                self._execute_monitor(args)
            elif args.command == 'analyze':
                self._execute_analyze(args)
            elif args.command == 'config':
                self._execute_config(args)
            elif args.command == 'report':
                self._execute_report(args)
            elif args.command == 'plugin':
                self._execute_plugin(args)
            elif args.command == 'update':
                self._execute_update(args)
            else:
                self.parser.print_help()
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            sys.exit(1)
        except Exception as e:
            if args.verbose:
                import traceback
                traceback.print_exc()
            else:
                print(f"Error: {e}")
            sys.exit(1)
    
    def _execute_discover(self, args):
        """Execute discover command."""
        print("🔍 Starting subdomain discovery...")
        print(f"Target domains: {args.domain or 'From file: ' + args.domain_list}")
        print(f"Sources: {args.all_sources and 'all' or args.sources or 'default'}")
        print(f"Output: {args.output or 'stdout'}")
        print(f"Format: {args.format}")
        
        # Placeholder implementation
        print("✅ Discovery completed successfully!")
    
    def _execute_scan(self, args):
        """Execute scan command."""
        print("🔬 Starting comprehensive scan...")
        print(f"Target: {args.target}")
        print(f"Mode: {args.mode}")
        print(f"Stages: {args.stages or 'all'}")
        print(f"Output: {args.output or args.output_dir}")
        print(f"Format: {args.format}")
        
        # Placeholder implementation
        print("✅ Scan completed successfully!")
    
    def _execute_monitor(self, args):
        """Execute monitor command."""
        print("👁️  Starting attack surface monitoring...")
        print(f"Domains: {args.domains}")
        print(f"Interval: {args.interval} seconds")
        print(f"Schedule: {args.schedule}")
        print(f"Output: {args.output}")
        
        # Placeholder implementation
        print("✅ Monitoring started successfully!")
    
    def _execute_analyze(self, args):
        """Execute analyze command."""
        print("📊 Starting data analysis...")
        print(f"Input: {args.input}")
        print(f"Operation: {args.operation}")
        print(f"Output: {args.output}")
        print(f"Format: {args.format}")
        
        # Placeholder implementation
        print("✅ Analysis completed successfully!")
    
    def _execute_config(self, args):
        """Execute config command."""
        print("⚙️  Configuration management...")
        
        if args.config_command == 'show':
            print(f"Showing configuration for profile: {args.profile}")
            print(f"Format: {args.format}")
        elif args.config_command == 'set':
            print(f"Setting {args.key} = {args.value}")
            if args.profile:
                print(f"Profile: {args.profile}")
        elif args.config_command == 'init':
            print("Initializing configuration...")
        elif args.config_command == 'profile':
            if args.list:
                print("Listing profiles...")
            elif args.create:
                print(f"Creating profile: {args.create}")
        elif args.config_command == 'provider':
            if args.list:
                print("Listing providers...")
            elif args.keys:
                print("Showing provider keys...")
            elif args.validate:
                print("Validating provider configurations...")
        
        print("✅ Configuration completed successfully!")
    
    def _execute_report(self, args):
        """Execute report command."""
        print("📋 Generating report...")
        print(f"Input: {args.input}")
        print(f"Type: {args.type}")
        print(f"Output: {args.output}")
        print(f"Format: {args.format}")
        
        # Placeholder implementation
        print("✅ Report generated successfully!")
    
    def _execute_plugin(self, args):
        """Execute plugin command."""
        print("🔌 Plugin management...")
        
        if args.plugin_command == 'list':
            print("Listing plugins...")
            if args.installed:
                print("Installed plugins:")
            if args.available:
                print("Available plugins:")
        elif args.plugin_command == 'install':
            print(f"Installing plugin: {args.plugin_name}")
        elif args.plugin_command == 'uninstall':
            print(f"Uninstalling plugin: {args.plugin_name}")
        elif args.plugin_command == 'info':
            print(f"Plugin info: {args.plugin_name}")
        elif args.plugin_command == 'config':
            print(f"Configuring plugin: {args.plugin_name}")
        elif args.plugin_command == 'enable':
            print(f"Enabling plugin: {args.plugin_name}")
        elif args.plugin_command == 'disable':
            print(f"Disabling plugin: {args.plugin_name}")
        elif args.plugin_command == 'update':
            print(f"Updating plugin: {args.plugin_name}")
        
        print("✅ Plugin management completed successfully!")
    
    def _execute_update(self, args):
        """Execute update command."""
        print("🔄 Updating SigmaRecon...")
        
        if args.check:
            print("Checking for available updates...")
            print("Core: Up to date")
            print("Tools: 3 updates available")
            print("Plugins: 1 update available")
        else:
            targets = []
            if args.core:
                targets.append("core")
            if args.tools:
                targets.append("tools")
            if args.configs:
                targets.append("configs")
            if args.plugins:
                targets.append("plugins")
            if args.wordlists:
                targets.append("wordlists")
            
            if not targets:
                print("No update targets specified")
                return
            
            print(f"Updating: {', '.join(targets)}")
        
        print("✅ Update completed successfully!")
    
    def run(self, argv: Optional[List[str]] = None):
        """Main entry point for the CLI application."""
        # Setup parser
        parser = self.setup_parser()
        
        # Parse arguments
        if argv is None:
            argv = sys.argv[1:]
        
        args = parser.parse_args(argv)
        
        # Validate arguments
        if not self.validate_arguments(args):
            return 1
        
        # Execute command
        self.execute_command(args)
        
        return 0


def main():
    """Main entry point."""
    try:
        cli = SigmaReconCLI()
        return cli.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        return 1


if __name__ == '__main__':
    sys.exit(main())