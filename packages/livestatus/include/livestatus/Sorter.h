// Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef Sorter_h
#define Sorter_h

class Row;

class Sorter {
public:
    Sorter() = default;
    virtual ~Sorter() = default;
};

#endif
