<center>
    <h1>
        OpenXR
    </h1>
</center>

## OpenXR 简介

XR对于对于很多人来说比较陌生，那XR是什么呢？OpenXR又是用来干什么的呢？

<img src="src\img\define.png" alt="define" style="zoom:30%;float:left" />

这里首先来说说这里的XR代表着什么。**XR其实就是AR，VR，MR的一个总称**。

> AR（Augmented Reality）增强显示：将现实场景和虚拟场景相结合的一种集成技术。通过将真实世界特定的画面或信息植入程序中，并对这些内容进行模拟、升级、补充、渲染，在应用AR技术的时候，这些被计算器处理的信息会在特定的场景被激发，与现实世界叠加，从而达到超越现实的感官体验。
>
> VR（Virtual Reality）虚拟现实：通过设备模拟一个完全虚拟的数字世界，通过VR眼睛和手柄等外设，能给使用者提供视觉、听觉等感官上的体验感。我们看到的一切场景和现实世界没有任何关联，所有的场景、事物都是由计算机生成的。
>
> MR（Mixed Reality）混合现实：MR是VR和AR的融合形态，能够将真实世界和虚拟世界进行融合，产生新的可视化环境。并且产生的虚拟动画能够和真实世界进行实时交互，而这是AR所不具备的。

官网对OpenXR的描述：

> OpenXR is a royalty-free, open standard that provides high-performance access to Augmented Reality (AR) and Virtual Reality (VR)—collectively known as XR—platforms and devices.

这里简单理解，OpenXR是一个免版税的，开放的标准，让应用能够更高效的使用AR和VR的平台和设备。

这里可能不能直观的了解OpenXR到底是用来干什么的，这里现有个简单的概念。**OpenXR是一套标准，定义了接口和使用方式，并且严格定义了每一个接口的功能，输入和输出，作用是让XR应用能够在XR平台或者设备上运行。**

### OpenXR的目的

<img src="src\img\OpenXR-Before.png" alt="OpenXR-Before" style="zoom:50%;float:left" />

首先来看当前的XR市场的情况，可以很明显的看到作为一个XR应用或者引擎的开发者，在当前XR市场群雄逐鹿的情况下，为了满足应用在多个平台上运行，需要应用基于多个平台的不同的SDK或者API进行不同的开发，大大加大了跨平台移植的难度和工作量，由于每一家的功能和能力不同，又会引入各种各样的问题。

<img src="src\img\OpenXR-After.png" alt="OpenXR-After" style="zoom:50%;float:left" />

在这种情况下作为开源标准制定组织中的老行家**khronos**在2019年提出了OpenXR这样的开放标准，来统一各个厂家的开发API。**目的是统一标准，简化移植的工作量，也能加快XR产业的发展。**

### 细说OpenXR

<img src="src\img\relationship.png" alt="relationship" style="zoom:50%;float:left" />

OpenXR作为应用和平台或者设备的桥梁，到底是怎么实现的？

这里将在不同的角度去阐述OpenXR的角色，分别是使用者OpenXR客户端，和实现者OpenXR平台端或者说是设备端。

#### OpenXR 客户端

作为应用端，当我们开发应用时，如果我们想在某个平台上运行，那么必须要知道这个平台开发的接口是什么。然后根据接口的规则定义进行应用的开发，那么OpenXR就是这套接口。OpenXR包含了开发者需要开发XR应用“所有”需要的平台接口函数。

> 由于目前不管是XR行业还是OpenXR都在快速发展中，所以很多系统新增的功能接口各家都在持续进行扩展和申请中，所以很多接口还是作为厂家独有的扩展进行使用，还没有合入OpenXR的公共接口中。

![OpenXR App](src\img\OpenXR App.png)

上图是OpenXR Demo中最基础的XR应用，此应用可以在支持OpenXR的所有平台上运行。其中有很多概念此处不做过多讲解，主要目的还是为了对OpenXR有一个清楚的概念。

上面主要是看蓝色部分的函数名，作为一个成熟的工程师，相信大家看到这些函数名已经对OpenXR有一个大致的概念。如果你是一个应用开发工程师，你只需要使用上述的API，并参照Demo使用的流程进行你的应用的开发，就能够使应用在OpenXR的平台上运行了。

###### 总结

简单来说对于应用开发者，我们只需要知道OpenXR定义了一套标准的API接口，我们可以通过Spec了解每一个API的定义，使用方法，参数和返回结果。根据OpenXR的Demo我们可以知道如何将这些接口结合起来，编写出自己的XR应用。

> 这里其实是OpenXR Native的使用方法，对于更多的开发者来说，大家开发XR应用的时候，更多的是使用游戏引擎，可能不会涉及到这些函数的使用，因为这些函数的调用已经由游戏引擎以自己的实现方式进行调用了。后续会有文档对Unity的OpenXR使用进行分析，主要是介绍用OpenXR实现Unity的SubSystem来实现Unity应用运行在OpenXR平台上。

#### OpenXR 平台端

作为平台其实就是去实现，对于应用来说，应用调用了同样的API，在不同的OpenXR平台上，返回的结果和实现的功能也应该是一样的。



## OpenXR API

## 相关资料 

* [OpenXR官网](https://www.khronos.org/openxr/)
* [OpenXR Sample Code: OpenXR-SDK-Source](https://github.com/KhronosGroup/OpenXR-SDK-Source)

