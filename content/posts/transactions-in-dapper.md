+++
date = '2025-03-20T09:39:47+05:30'
draft = false
title = 'Transactions in Dapper'
tags = ['dotnet','dapper']
categories = ['programming']
+++

Isn't it already described in Dapper docs? Sure it is. Why do I bother to write this? Am I just wtiting it for the sake of "posting"? No, I am not. Actually, I was trying to write the code by using Dapper's docs. Unfortunately, I ran into a few bugs. I am using .NET 9, by the way and this is not even a blog post; it's just a code snippet. I thought I should share it, may be someone else is facing the same problem as me.

```cs
using IDbConnection connection = new SqlConnection(_connectionString);

connection.Open();

using var tran = connection.BeginTransaction();

int trackEntryId=0;  // I need trackEntryId outside the try block

try
{
    string trackEntryQuery = @"insert into TrackEntries(EntryDate,SleptAt,WokeUpAt,NapInMinutes,TotalWorkInMinutes)
                 values (@EntryDate,@SleptAt,@WokeUpAt,@NapInMinutes,@TotalWorkInMinutes);
                 select scope_identity();
                 ";
    trackEntryId = await connection.ExecuteScalarAsync<int>(trackEntryQuery, trackEntryToCreate,transaction:tran);

    if (!string.IsNullOrWhiteSpace(trackEntryToCreate.Remarks))
    {
        string trackEntryRemarkQuery = @"insert into TrackEntryRemarks (TrackEntryId,Remarks)
          values(@TrackEntryId,@Remarks);";
        await connection.ExecuteAsync(trackEntryRemarkQuery, new { TrackEntryId = trackEntryId, trackEntryToCreate.Remarks},transaction:tran);
    }
    tran.Commit();
}
catch
{
    tran.Rollback();
    throw;
}
```

I was getting errors because:

- I never opened the connection. I never had to open the connection with Dapper before, and it was working fine until I used transactions.
- I was't passing `transaction:tran` to `ExecuteScalarAsync()` or `ExecuteAsync()`.
