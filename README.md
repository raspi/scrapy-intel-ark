# scrapy-intel-ark
Web crawler for Intel ARK ([ark.intel.com](https://ark.intel.com))

## Requirements

* Python
* [Scrapy](https://scrapy.org/)

## CPU specs spider

Downloads all CPU specifications as JSON files.

    scrapy crawl cpuspecs
    
Everything is downloaded to `items/cpuspecs` directory. Each CPU is in it's own socket subdirectory. 

After crawling `_legend.json` is written which has explanations for the fields.

The prices will be written separately to `cpuprices.json`.

### Notes
* 30 day cache is used in `settings.py`
* Some product information pages do **not** contain socket information, so they are written to `_unknown/` directory


## _legend.json

```json
{
  "Essentials": {
    "ProductGroup": "Product Collection",
    "CodeNameText": "Code Name",
    "MarketSegment": "Vertical Segment",
    "ProcessorNumber": "Processor Number",
    "OffRoadmap": "Off Roadmap",
    "StatusCodeText": "Status",
    "BornOnDate": "Launch Date",
    "Lithography": "Lithography"
  },
  "Performance": {
    "CoreCount": "# of Cores",
    "ThreadCount": "# of Threads",
    "ClockSpeed": "Processor Base Frequency",
    "ClockSpeedMax": "Max Turbo Frequency",
    "Cache": "Cache",
    "Bus": "Bus Speed",
    "MaxTDP": "TDP",
    "ConfigTDPMaxFrequency": "Configurable TDP-up Frequency",
    "ConfigTDPMax": "Configurable TDP-up",
    "ConfigTDPMinFrequency": "Configurable TDP-down Frequency",
    "ConfigTDPMin": "Configurable TDP-down"
  },
  "Supplemental Information": {
    "Embedded": "Embedded Options Available"
  },
  "Memory Specifications": {
    "MaxMem": "Max Memory Size (dependent on memory type)",
    "MemoryTypes": "Memory Types",
    "NumMemoryChannels": "Max # of Memory Channels",
    "MaxMemoryBandwidth": "Max Memory Bandwidth",
    "ECCMemory": "ECC Memory Supported"
  },
  "Processor Graphics": {
    "ProcessorGraphicsModelId": "Processor Graphics",
    "GraphicsFreq": "Graphics Base Frequency",
    "GraphicsMaxFreq": "Graphics Max Dynamic Frequency",
    "GraphicsMaxMem": "Graphics Video Max Memory",
    "GraphicsOutput": "Graphics Output",
    "GraphicsExecutionUnits": "Execution Units",
    "Graphics4KSupportLevel": "4K Support",
    "GraphicsMaxResolutionHDMI": "Max Resolution (HDMI 1.4)",
    "GraphicsMaxResolutionDP": "Max Resolution (DP)",
    "GraphicsMaxResolutionIFP": "Max Resolution (eDP - Integrated Flat Panel)",
    "GraphicsDirectXSupport": "DirectX* Support",
    "GraphicsOpenGLSupport": "OpenGL* Support",
    "QuickSyncVideo": "Quick Sync Video",
    "CVTHD": "Clear Video HD Technology",
    "ClearVideoTechnology": "Clear Video Technology",
    "NumDisplaysSupported": "# of Displays Supported",
    "GraphicsDeviceId": "Device ID"
  },
  "Expansion Options": {
    "PCIExpressRevision": "PCI Express Revision",
    "PCIExpressConfigs": "PCI Express Configurations",
    "NumPCIExpressPorts": "Max # of PCI Express Lanes"
  },
  "Package Specifications": {
    "SocketsSupported": "Sockets Supported",
    "MaxCPUs": "Max CPU Configuration",
    "ThermalJunctionRateCode": "TJUNCTION",
    "PackageSize": "Package Size"
  },
  "Advanced Technologies": {
    "OptaneMemorySupport": "Optane Memory Supported",
    "SpeedShiftTechVersion": "Speed Shift Technology",
    "ThermalVelocityBoostVersion": "Thermal Velocity Boost",
    "TBTVersion": "Turbo Boost Technology",
    "VProTechnology": "vPro Platform Eligibility",
    "HyperThreading": "Hyper-Threading Technology",
    "VTX": "Virtualization Technology (VT-x)",
    "VTD": "Virtualization Technology for Directed I/O (VT-d)",
    "ExtendedPageTables": "VT-x with Extended Page Tables (EPT)",
    "TransactionalSynchronizationExtensionVersion": "TSX-NI",
    "EM64": "64",
    "InstructionSet": "Instruction Set",
    "InstructionSetExtensions": "Instruction Set Extensions",
    "MyWiFiTech": "My WiFi Technology",
    "HaltState": "Idle States",
    "SpeedstepTechnology": "Enhanced SpeedStep Technology",
    "ThermalMonitoring2Indicator": "Thermal Monitoring Technologies",
    "FlexMemoryTechnology": "Flex Memory Access",
    "IdentityProtectionTechVersion": "Identity Protection Technology",
    "StableImagePlatformProgramVersion": "Stable Image Platform Program (SIPP)"
  },
  "Security & Reliability": {
    "AESTech": "AES New Instructions",
    "SecureKeyTechVersion": "Secure Key",
    "SoftwareGuardExtensions": "Software Guard Extensions ( SGX)",
    "MemoryProtectionExtensionsVersion": "Memory Protection Extensions ( MPX)",
    "OSGuardTechVersion": "OS Guard",
    "TXT": "Trusted Execution Technology",
    "ExecuteDisable": "Execute Disable Bit",
    "DeviceProtectionTechBootGuardVersion": "Boot Guard"
  },
  "I/O Specifications": {
    "NumUSBPorts": "# of USB Ports",
    "USBRevision": "USB Revision",
    "NumSATAPorts": "Total # of SATA Ports",
    "IntegratedLAN": "Integrated LAN",
    "IntegratedIDE": "Integrated IDE",
    "GeneralPurposeIO": "General Purpose IO",
    "UART": "UART",
    "SATA6PortCount": "Max # of SATA 6.0 Gb/s Ports"
  },
  "Networking Specifications": {
    "NetworkInterfaces": "Interfaces Supported"
  },
  "Discrete Graphics": {
    "DiscreteGraphicsModelId": "Graphics Name",
    "DiscreteGraphicsMaxFreqMhz": "Graphics Max Dynamic Frequency",
    "DiscreteGraphicsFreqMhz": "Graphics Base Frequency",
    "DiscreteGraphicsComputeUnitCount": "Compute Units",
    "DiscreteGraphicsDedicatedMemoryBandwidth": "Graphics Memory Bandwidth",
    "DiscreteGraphicsDedicatedMemoryInterface": "Graphics Memory Interface",
    "DiscreteGraphicsOutputOptions": "Graphics Output",
    "DiscreteGraphics4KSupportLevel": "4K Support",
    "DiscreteGraphicsMaxResolutionHDMI": "Max Resolution (HDMI)",
    "DiscreteGraphicsMaxResolutionDP": "Max Resolution (DP)",
    "DiscreteGraphicsMaxResolutionIFP": "Max Resolution (eDP - Integrated Flat Panel)",
    "DiscreteGraphicsDirectXSupport": "DirectX* Support",
    "DiscreteGraphicsVulkanSupport": "Vulkan* Support",
    "DiscreteGraphicsOpenGLSupport": "OpenGL* Support",
    "DiscreteGraphicsH264Hardware": "H.264 Hardware Encode/Decode",
    "DiscreteGraphicsH265HardwareDesc": "H.265 (HEVC) Hardware Encode/Decode",
    "DiscreteNumDisplaysSupported": "# of Displays Supported"
  }
}
```
