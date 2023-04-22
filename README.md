About
-----

Python Module for manipulating SMPTE timecode, with negative frame number support.
`stimecode` is for 'signed timecode'.

```python
    from stimecode import STimecode
    from timecode import Timecode

    tc1 = STimecode('29.97', '00:00:20;00')
    tc2 = Timecode('24', '00:00:30:00')
    tc3 = tc1 - tc2
    assert tc3.framerate == '29.97'
    assert tc3.frame_number == -120
	assert tc3.frames == 121
    assert tc3 == '-00:00:00;04'
	
	tc4 = tc2 - tc1
    assert tc4.framerate == '24'
    assert tc4.frame_number == 120
    assert tc4 == '00:00:05:00'
```

This library is a fork of the [timecode](https://github.com/eoyilmaz/timecode).
Although `STimecode` is a child class of `Timecode`, `STimecode` overloads all attributes of 
`Timecode`.

There are destructive deviation from original `timecode` in the following points:

- `__init__` accepts `frame_number` instead of `frames`.
- Does not arise an error even `frame_number` being negative.
- Results of multiplication and division between timecodes are not same to these of `timecode`.
  While the original `timecode` caluculates by frames, `stimecode` calculates by `frame_numbers`.
- Arthmetics between two timecodes with different `framerate` will return the `framerate`
  of first term. (Ex: `framerate` of `tc3 = tc1 + tc2` is that of `tc1`)

Other defferences are:

- Arthmetics between `stimecode` and `timecode` is supported. Result is always `stimecode`.
- `__neg__` operator and reflected arthmetics operators such as `__radd__` defined.
- `frames` is still supported.

```python
    from stimecode import STimecode
    from timecode import Timecode

    tc1 = STimecode('29.97', '00:00:20;00')
    tc2 = Timecode('24', '00:00:30:00')
    tc3 = tc1 - tc2
    assert tc3.framerate == '29.97'
    assert tc3.frame_number == -120
	assert tc3.frames == 121
    assert tc3 == '-00:00:00;04'
	
	tc4 = tc2 - tc1
    assert tc4.framerate == '24'
    assert tc4.frame_number == 120
    assert tc4 == '00:00:05:00'
```

The rest of usages are same to `timecode`, see [readme of timecode](https://github.com/eoyilmaz/timecode).


## License

The MIT License (MIT) Copyright (c) K. Chinzei (kchinzei@gmail.com) Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
