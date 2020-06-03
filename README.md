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

## Single CPU specs spider
    
    crawl onecpuspec -a url="https://ark.intel.com/content/www/us/en/ark/products/82764/intel-xeon-processor-e5-1630-v3-10m-cache-3-70-ghz.html"

See **CPU specs spider** for info.
    

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
    "StatusCodeText": "Status",
    "BornOnDate": "Launch Date",
    "Lithography": "Lithography",
    "CertifiedUseConditions": "Use Conditions",
    "ExpectedDiscontinuanceDate": "Expected Discontinuance",
    "ItemsIncluded": "Included Items",
    "WarrantyLengthYears": "Warranty Period"
  },
  "Performance": {
    "CoreCount": "# of Cores",
    "ThreadCount": "# of Threads",
    "ClockSpeed": "Processor Base Frequency",
    "ClockSpeedMax": "Max Turbo Frequency",
    "Cache": "Cache",
    "Bus": "Bus Speed",
    "MaxTDP": "TDP",
    "FSBParity": "FSB Parity",
    "CoreVoltage": "VID Voltage Range",
    "ScenarioDesignPower": "Scenario Design Power (SDP)",
    "TurboBoostTech2MaxFreq": "Turbo Boost Technology 2.0 Frequency",
    "BusNumPorts": "# of QPI Links",
    "ConfigTDPMin": "Configurable TDP-down",
    "ConfigTDPMinFrequency": "Configurable TDP-down Frequency",
    "BurstFrequency": "Burst Frequency",
    "TurboBoostMaxTechMaxFreq": "Turbo Boost Max Technology 3.0 Frequency",
    "UltraPathInterconnectLinks": "# of UPI Links",
    "ConfigTDPMaxFrequency": "Configurable TDP-up Frequency",
    "ConfigTDPMax": "Configurable TDP-up",
    "ThermalVelocityBoostFreq": "Thermal Velocity Boost Frequency",
    "SingleCoreBaseFrequency": "Processor Single Core Base Frequency",
    "SingleCoreTDP": "Single Core TDP"
  },
  "Supplemental Information": {
    "Embedded": "Embedded Options Available",
    "null": "Datasheet",
    "ProductDescription": "Description",
    "ProductBriefUrl": "Product Brief",
    "DatasheetUrl": "Datasheet"
  },
  "Memory Specifications": {
    "MaxMem": "Max Memory Size (dependent on memory type)",
    "MemoryTypes": "Memory Types",
    "NumMemoryChannels": "Max # of Memory Channels",
    "MaxMemoryBandwidth": "Max Memory Bandwidth",
    "ECCMemory": "ECC Memory Supported",
    "PhysicalAddressExtension": "Physical Address Extensions",
    "MemoryMaxSpeedMhz": "Maximum Memory Speed",
    "OptaneDCPersistentMemoryVersion": "Optane DC Persistent Memory Supported"
  },
  "Processor Graphics": {
    "ProcessorGraphicsModelId": "Processor Graphics",
    "GraphicsFreq": "Graphics Base Frequency",
    "GraphicsMaxFreq": "Graphics Max Dynamic Frequency",
    "QuickSyncVideo": "Quick Sync Video",
    "InTru3D": "InTru 3D Technology",
    "FDI": "Flexible Display Interface ( FDI)",
    "CVTHD": "Clear Video HD Technology",
    "NumDisplaysSupported": "# of Displays Supported",
    "GraphicsDeviceId": "Device ID",
    "GraphicsOutput": "Graphics Output",
    "ClearVideoTechnology": "Clear Video Technology",
    "LicenseRequired": "Macrovision* License Required",
    "GraphicsMaxMem": "Graphics Video Max Memory",
    "GraphicsMaxResolutionHDMI": "Max Resolution (HDMI 1.4)",
    "GraphicsMaxResolutionDP": "Max Resolution (DP)",
    "GraphicsMaxResolutionIFP": "Max Resolution (eDP - Integrated Flat Panel)",
    "GraphicsMaxResoluionVGA": "Max Resolution (VGA)",
    "GraphicsDirectXSupport": "DirectX* Support",
    "GraphicsOpenGLSupport": "OpenGL* Support",
    "Graphics4KSupportLevel": "4K Support",
    "GraphicsExecutionUnits": "Execution Units",
    "GraphicsBurstFrequency": "Graphics Burst Frequency",
    "GraphicsMaxRefreshRateHz": "Max Refresh Rate",
    "EmbeddedDramMB": "eDRAM"
  },
  "Expansion Options": {
    "PCIExpressRevision": "PCI Express Revision",
    "PCIExpressConfigs": "PCI Express Configurations",
    "NumPCIExpressPorts": "Max # of PCI Express Lanes",
    "ScalableSockets": "Scalability",
    "PCISupport": "PCI Support"
  },
  "Package Specifications": {
    "SocketsSupported": "Sockets Supported",
    "MaxCPUs": "Max CPU Configuration",
    "ThermalSolutionSpecification": "Thermal Solution Specification",
    "TCase": "TCASE",
    "PackageSize": "Package Size",
    "ThermalJunctionRateCode": "TJUNCTION",
    "DieSize": "Processing Die Size",
    "TransistorCount": "# of Processing Die Transistors",
    "OperatingTemperature": "Operating Temperature Range",
    "OperatingTemperatureMax": "Operating Temperature (Maximum)",
    "OperatingTemperatureMin": "Operating Temperature (Minimum)",
    "BracketHeight": "Bracket Height"
  },
  "Advanced Technologies": {
    "TBTVersion": "Turbo Boost Technology",
    "VProTechnology": "vPro Platform Eligibility",
    "HyperThreading": "Hyper-Threading Technology",
    "VTX": "Virtualization Technology (VT-x)",
    "VTD": "Virtualization Technology for Directed I/O (VT-d)",
    "ExtendedPageTables": "VT-x with Extended Page Tables (EPT)",
    "TransactionalSynchronizationExtensionVersion": "Transactional Synchronization Extensions",
    "EM64": "64",
    "InstructionSet": "Instruction Set",
    "InstructionSetExtensions": "Instruction Set Extensions",
    "HaltState": "Idle States",
    "SpeedstepTechnology": "Enhanced SpeedStep Technology",
    "ThermalMonitoring2Indicator": "Thermal Monitoring Technologies",
    "IdentityProtectionTechVersion": "Identity Protection Technology",
    "MyWiFiTech": "My WiFi Technology",
    "WiMAX": "4G WiMAX Wireless Technology",
    "DemandBasedSwitching": "Demand Based Switching",
    "FastMemoryTechnology": "Fast Memory Access",
    "FlexMemoryTechnology": "Flex Memory Access",
    "VTI": "Virtualization Technology for Itanium (VT-i)",
    "OptaneMemorySupport": "Optane Memory Supported",
    "StableImagePlatformProgramVersion": "Stable Image Platform Program (SIPP)",
    "SpeedShiftTechVersion": "Speed Shift Technology",
    "SmartResponseTechVersion": "Smart Response Technology",
    "ThermalVelocityBoostVersion": "Thermal Velocity Boost",
    "TurboBoostMaxTechVersion": "Turbo Boost Max Technology 3.0",
    "RapidStorageTech": "Rapid Storage Technology",
    "SecureBootTechVersion": "Secure Boot",
    "HDAudioTechnology": "HD Audio Technology",
    "SmartConnectVersion": "Smart Connect Technology",
    "AMTVersion": "ME Firmware Version",
    "MatrixStorageTechnology": "Matrix Storage Technology",
    "AVX512FusedMultiplyAddUnits": "# of AVX-512 FMA Units",
    "DeepLearningBoostVersion": "Deep Learning Boost ( DL Boost)",
    "ResourceDirectorTechVersion": "Resource Director Technology ( RDT)",
    "QuickAssistTechnology": "Integrated Quick Assist Technology",
    "VolumeManagementDeviceVersion": "Volume Management Device (VMD)",
    "SmartIdleTechVersion": "Smart Idle Technology",
    "QuickResumeTechnology": "Quick Resume Technology",
    "QuietSystemTechnology": "Quiet System Technology",
    "AC97Technology": "AC97 Technology",
    "IOAccelerationTechnology": "I/O Acceleration Technology",
    "InstructionReplayTechVersion": "Instruction Replay Technology",
    "SstPerformanceProfileVersion": "Speed Select Technology - Performance Profile",
    "SstBaseFrequencyOptionVersion": "Speed Select Technology - Base Frequency",
    "OmniPathArchitectureVersion": "Integrated Omni-Path Architecture ( OPA)"
  },
  "Security & Reliability": {
    "AESTech": "AES New Instructions",
    "SecureKeyTechVersion": "Secure Key",
    "TXT": "Trusted Execution Technology",
    "ExecuteDisable": "Execute Disable Bit",
    "AntiTheftTechnology": "Anti-Theft Technology",
    "SoftwareGuardExtensions": "Software Guard Extensions ( SGX)",
    "MemoryProtectionExtensionsVersion": "Memory Protection Extensions ( MPX)",
    "OSGuardTechVersion": "OS Guard",
    "DeviceProtectionTechBootGuardVersion": "Boot Guard",
    "RunSureTechnologyVersion": "Run Sure Technology",
    "ModeBasedExecutionControlVersion": "Mode-based Execute Control (MBE)"
  },
  "Performance Specifications": {
    "CoreCount": "# of Cores",
    "ThreadCount": "# of Threads",
    "ClockSpeed": "Processor Base Frequency",
    "Cache": "Cache",
    "Bus": "Bus Speed",
    "FSBParity": "FSB Parity",
    "MaxTDP": "TDP",
    "CoreVoltage": "VID Voltage Range",
    "ScenarioDesignPower": "Scenario Design Power (SDP)",
    "ClockSpeedMax": "Max Turbo Frequency",
    "BusNumPorts": "# of QPI Links",
    "TurboBoostTech2MaxFreq": "Turbo Boost Technology 2.0 Frequency",
    "ConfigTDPMin": "Configurable TDP-down",
    "BurstFrequency": "Burst Frequency",
    "TurboBoostMaxTechMaxFreq": "Turbo Boost Max Technology 3.0 Frequency",
    "UltraPathInterconnectLinks": "# of UPI Links",
    "ConfigTDPMinFrequency": "Configurable TDP-down Frequency",
    "FSBsSupported": "Supported FSBs",
    "ConfigTDPMaxFrequency": "Configurable TDP-up Frequency",
    "ConfigTDPMax": "Configurable TDP-up"
  },
  "I/O Specifications": {
    "NumUSBPorts": "# of USB Ports",
    "USBRevision": "USB Revision",
    "NumSATAPorts": "Total # of SATA Ports",
    "IntegratedLAN": "Integrated LAN",
    "IntegratedWifi": "Integrated Wireless",
    "GeneralPurposeIO": "General Purpose IO",
    "UART": "UART",
    "SATA6PortCount": "Max # of SATA 6.0 Gb/s Ports",
    "IntegratedIDE": "Integrated IDE",
    "USBConfigurationDescription": "USB Configuration"
  },
  "Networking Specifications": {
    "NetworkInterfaces": "Interfaces Supported",
    "BasebandFunctions": "Baseband Functions",
    "RadioFreqTransceiver": "RF Transceiver",
    "RadioFreqTransceiverFunctions": "RF Transceiver Functions",
    "ProtocolStack": "Protocol Stack"
  },
  "Discrete Graphics": {
    "DiscreteGraphicsFreqMhz": "Graphics Base Frequency",
    "DiscreteGraphicsModelId": "Graphics Name",
    "DiscreteGraphicsMaxFreqMhz": "Graphics Max Dynamic Frequency",
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
