<center>
    <h1>
        Compositor Time
    </h1>
</center>

## About Time

### App Time

**src\xrt\auxiliary\util\u_pacing_app.c**

```c
struct
{
	uint64_t predicted_ns;
	uint64_t wait_woke_ns;
	uint64_t begin_ns;
	uint64_t delivered_ns;
	uint64_t gpu_done_ns;
} when;
```

* `predicted_ns`: 调用**xrWaitFrame**的内部调用**predict_frame**的时间。
* `wait_woke_ns`: 调用**xrWaitFrame**返回的时间。
* `begin_ns`: 调用**xrBeginFrame**的时间。
* `delivered_ns`: 调用**xrEndFrame**的时间。
* `.`: App端图像处理完成的时间。

```c
struct
{
	//! App time between wait returning and begin being called.
	uint64_t cpu_time_ns;
	//! Time between begin and frame data being delivered.
	uint64_t draw_time_ns;
	//! Time between the frame data being delivered and GPU completing.
	uint64_t wait_time_ns;
	//! Extra time between end of draw time and when the compositor wakes up.
	uint64_t margin_ns;
} app; //!< App statistics.
```

* `cpu_time_ns`: ( = `begin_ns` - `wait_woke_ns` ) 即调用**xrWaitFrame**返回后到**xrBeginFrame**之间的时间。
* `draw_time_ns`: ( = `delivered_ns` - `begin_ns` ) 即调用**xrBeginFrame**到调用**xrEndFrame**的时间。
* `wait_time_ns`: ( = `gpu_done_ns` - `delivered_ns` ) 即调用**xrEndFrame**到渲染完的时间。
* `margin_ns`: 2ms 固定值，表示App绘制完成后到被Runtime使用的时间。

```c
struct
{
	//! The last display time that the thing driving this helper got.
	uint64_t predicted_display_time_ns;
	//! The last display period the hardware is running at.
	uint64_t predicted_display_period_ns;
	//! The extra time needed by the thing driving this helper.
	uint64_t extra_ns;
} last_input;
```

* `predicted_display_time_ns`: 预测的显示时间。
* `predicted_display_period_ns`: 预测的每一帧的显示间隔。
* `extra_ns`: Runtime compose到预测显示的时间。

 ```mermaid
 gantt
 title Monado Time Line
 dateFormat YYYY-MM-DD-HH-mm
 axisFormat %H%M
 section App
 xrWaitFrame: active, a, 2000-01-01-00-00, 2h
 xrBeginFrame: milestone, b, 2000-01-01-03-00,1m
 app render: active, c, 2000-01-01-04-00, 4h
 xrEndFrame: milestone, d, 2000-01-01-09-00, 1m
 runtime render: active, e, 2000-01-01-10-00, 30m

 xrWaitFrame: active, a, 2000-01-01-12-00, 2h
 xrBeginFrame: milestone, b, 2000-01-01-15-00,1m

 section Runtime
 compose: active, a, 2000-01-01-11-00, 1.5h
 display: active, t1, 2000-01-01-13-00,30m

 section Time Point
 predicted_ns: milestone, t1, 2000-01-01-00-00,1m
 wait_woke_ns: milestone, t2, 2000-01-01-02-00,1m
 begin_ns: milestone, t3, 2000-01-01-03-00, 1m
 delivered_ns: milestone, t4, 2000-01-01-09-00, 1m
 gpu_done_ns: milestone, t4, 2000-01-01-10-30, 1m

 section Period
 cpu_time_ns: active, a, 2000-01-01-02-00, 1h
 draw_time_ns: active, a, 2000-01-01-03-00, 6h
 wait_time_ns: active, a, 2000-01-01-09-00, 1.5h
 margin_ns: active, a, 2000-01-01-10-30, 30m
 extra_ns: active, a, 2000-01-01-11-00, 2h
 ```

