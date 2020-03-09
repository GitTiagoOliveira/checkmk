// Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
// This file is part of Checkmk (https://checkmk.com). It is subject to the
// terms and conditions defined in the file COPYING, which is part of this
// source code package.

#ifndef OffsetTimeColumn_h
#define OffsetTimeColumn_h

#include "config.h"  // IWYU pragma: keep
#include <chrono>
#include "TimeColumn.h"
class Row;

class OffsetTimeColumn : public TimeColumn {
public:
    using TimeColumn::TimeColumn;

private:
    [[nodiscard]] std::chrono::system_clock::time_point getRawValue(
        Row row) const override;
};

#endif  // OffsetTimeColumn_h
